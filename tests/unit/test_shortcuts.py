import mock

import pytest

from openapi_core.shortcuts import (
    validate_parameters, validate_body, validate_data,
)


class ResultMock(object):

    def __init__(
            self, body=None, parameters=None, data=None, error_to_raise=None):
        self.body = body
        self.parameters = parameters
        self.data = data
        self.error_to_raise = error_to_raise

    def raise_for_errors(self):
        if self.error_to_raise is not None:
            raise self.error_to_raise

        if self.parameters is not None:
            return self.parameters

        if self.data is not None:
            return self.data


class FactoryClassMock(object):

    _instances = {}

    def __new__(cls, obj):
        if obj not in cls._instances:
            cls._instances[obj] = object.__new__(cls)
        return cls._instances[obj]

    def __init__(self, obj):
        self.obj = obj


class TestValidateParameters(object):

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_no_request_factory(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        parameters = mock.sentinel.parameters
        mock_validate.return_value = ResultMock(parameters=parameters)

        result = validate_parameters(spec, request)

        assert result == parameters
        mock_validate.aasert_called_once_with(request)

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_no_request_factory_error(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        mock_validate.return_value = ResultMock(error_to_raise=ValueError)

        with pytest.raises(ValueError):
            validate_parameters(spec, request)

        mock_validate.aasert_called_once_with(request)

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_request_factory(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        parameters = mock.sentinel.parameters
        mock_validate.return_value = ResultMock(parameters=parameters)
        request_factory = FactoryClassMock

        result = validate_parameters(spec, request, request_factory)

        assert result == parameters
        mock_validate.assert_called_once_with(
            FactoryClassMock(request),
        )

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_request_factory_error(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        mock_validate.return_value = ResultMock(error_to_raise=ValueError)
        request_factory = FactoryClassMock

        with pytest.raises(ValueError):
            validate_parameters(spec, request, request_factory)

        mock_validate.assert_called_once_with(
            FactoryClassMock(request),
        )


class TestValidateBody(object):

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_no_request_factory(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        body = mock.sentinel.body
        mock_validate.return_value = ResultMock(body=body)

        result = validate_body(spec, request)

        assert result == body
        mock_validate.aasert_called_once_with(request)

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_no_request_factory_error(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        mock_validate.return_value = ResultMock(error_to_raise=ValueError)

        with pytest.raises(ValueError):
            validate_body(spec, request)

        mock_validate.aasert_called_once_with(request)

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_request_factory(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        body = mock.sentinel.body
        mock_validate.return_value = ResultMock(body=body)
        request_factory = FactoryClassMock

        result = validate_body(spec, request, request_factory)

        assert result == body
        mock_validate.assert_called_once_with(
            FactoryClassMock(request),
        )

    @mock.patch('openapi_core.shortcuts.RequestValidator.validate')
    def test_request_factory_error(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        mock_validate.return_value = ResultMock(error_to_raise=ValueError)
        request_factory = FactoryClassMock

        with pytest.raises(ValueError):
            validate_body(spec, request, request_factory)

        mock_validate.assert_called_once_with(
            FactoryClassMock(request),
        )


class TestvalidateData(object):

    @mock.patch('openapi_core.shortcuts.ResponseValidator.validate')
    def test_no_factories(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        response = mock.sentinel.response
        data = mock.sentinel.data
        mock_validate.return_value = ResultMock(data=data)

        result = validate_data(spec, request, response)

        assert result == data
        mock_validate.aasert_called_once_with(request, response)

    @mock.patch('openapi_core.shortcuts.ResponseValidator.validate')
    def test_no_factories_error(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        response = mock.sentinel.response
        mock_validate.return_value = ResultMock(error_to_raise=ValueError)

        with pytest.raises(ValueError):
            validate_data(spec, request, response)

        mock_validate.aasert_called_once_with(request, response)

    @mock.patch('openapi_core.shortcuts.ResponseValidator.validate')
    def test_factories(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        response = mock.sentinel.response
        data = mock.sentinel.data
        mock_validate.return_value = ResultMock(data=data)
        request_factory = FactoryClassMock
        response_factory = FactoryClassMock

        result = validate_data(
            spec, request, response,
            request_factory, response_factory,
        )

        assert result == data
        mock_validate.assert_called_once_with(
            FactoryClassMock(request),
            FactoryClassMock(response),
        )

    @mock.patch('openapi_core.shortcuts.ResponseValidator.validate')
    def test_factories_error(self, mock_validate):
        spec = mock.sentinel.spec
        request = mock.sentinel.request
        response = mock.sentinel.response
        mock_validate.return_value = ResultMock(error_to_raise=ValueError)
        request_factory = FactoryClassMock
        response_factory = FactoryClassMock

        with pytest.raises(ValueError):
            validate_data(
                spec, request, response,
                request_factory, response_factory,
            )

        mock_validate.assert_called_once_with(
            FactoryClassMock(request),
            FactoryClassMock(response),
        )
