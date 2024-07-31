<!-- Documentación códigos documentation master file, created by
sphinx-quickstart on Sun Jul 28 15:42:47 2024.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->

# Documentación códigos documentation

Add your content using `reStructuredText` syntax. See the
[reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)
documentation for details.

# Contents:

* [main module](main.md)
  * [`start_streamlit_service()`](main.md#main.start_streamlit_service)
* [model_service module](model_service.md)
  * [`PredictionRequest`](model_service.md#model_service.PredictionRequest)
    * [`PredictionRequest.Config`](model_service.md#model_service.PredictionRequest.Config)
      * [`PredictionRequest.Config.protected_namespaces`](model_service.md#model_service.PredictionRequest.Config.protected_namespaces)
    * [`PredictionRequest.angulo`](model_service.md#model_service.PredictionRequest.angulo)
    * [`PredictionRequest.model_computed_fields`](model_service.md#model_service.PredictionRequest.model_computed_fields)
    * [`PredictionRequest.model_config`](model_service.md#model_service.PredictionRequest.model_config)
    * [`PredictionRequest.model_fields`](model_service.md#model_service.PredictionRequest.model_fields)
    * [`PredictionRequest.model_folder`](model_service.md#model_service.PredictionRequest.model_folder)
    * [`PredictionRequest.model_name`](model_service.md#model_service.PredictionRequest.model_name)
    * [`PredictionRequest.par`](model_service.md#model_service.PredictionRequest.par)
    * [`PredictionRequest.window_size`](model_service.md#model_service.PredictionRequest.window_size)
  * [`load_model_and_scaler()`](model_service.md#model_service.load_model_and_scaler)
  * [`predict()`](model_service.md#model_service.predict)
  * [`read_root()`](model_service.md#model_service.read_root)
  * [`start_service()`](model_service.md#model_service.start_service)
* [prediction_service module](prediction_service.md)
  * [`DataRequest`](prediction_service.md#prediction_service.DataRequest)
    * [`DataRequest.angulo`](prediction_service.md#prediction_service.DataRequest.angulo)
    * [`DataRequest.identificador`](prediction_service.md#prediction_service.DataRequest.identificador)
    * [`DataRequest.model_computed_fields`](prediction_service.md#prediction_service.DataRequest.model_computed_fields)
    * [`DataRequest.model_config`](prediction_service.md#prediction_service.DataRequest.model_config)
    * [`DataRequest.model_fields`](prediction_service.md#prediction_service.DataRequest.model_fields)
    * [`DataRequest.par`](prediction_service.md#prediction_service.DataRequest.par)
    * [`DataRequest.reset`](prediction_service.md#prediction_service.DataRequest.reset)
  * [`ModelUpdateRequest`](prediction_service.md#prediction_service.ModelUpdateRequest)
    * [`ModelUpdateRequest.model_computed_fields`](prediction_service.md#prediction_service.ModelUpdateRequest.model_computed_fields)
    * [`ModelUpdateRequest.model_config`](prediction_service.md#prediction_service.ModelUpdateRequest.model_config)
    * [`ModelUpdateRequest.model_fields`](prediction_service.md#prediction_service.ModelUpdateRequest.model_fields)
    * [`ModelUpdateRequest.model_folder`](prediction_service.md#prediction_service.ModelUpdateRequest.model_folder)
    * [`ModelUpdateRequest.model_name`](prediction_service.md#prediction_service.ModelUpdateRequest.model_name)
    * [`ModelUpdateRequest.window_size`](prediction_service.md#prediction_service.ModelUpdateRequest.window_size)
  * [`get_data()`](prediction_service.md#prediction_service.get_data)
  * [`health_check()`](prediction_service.md#prediction_service.health_check)
  * [`receive_data()`](prediction_service.md#prediction_service.receive_data)
  * [`start_service()`](prediction_service.md#prediction_service.start_service)
  * [`update_model()`](prediction_service.md#prediction_service.update_model)
* [test_model module](test_model.md)
  * [`check_server_status()`](test_model.md#test_model.check_server_status)
  * [`prepare_data_for_prediction()`](test_model.md#test_model.prepare_data_for_prediction)
  * [`process_excel_and_send_data()`](test_model.md#test_model.process_excel_and_send_data)
* [visualization_service module](visualization_service.md)
