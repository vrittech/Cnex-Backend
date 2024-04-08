from . import frontend_setting
mapping = {
    "service_booked!":{
        "model_name":"Product",
        "admin_message":"A new sample ({sample_id}) has been requested for testing by user ({username})",
        "path":frontend_setting.smu_sample_request_details,
        "user_message":"Your sample ({refrence_number}) has been submitted successfully",
    },
    "payment_confirmed":{
        "model_name":"SuperVisorSampleForm",
        "path":frontend_setting.supervisor_sample_request_details,
        "admin_message":"New sample ({sample_lab_id}) has been assigned",
        "user_message":"None",
    },
    "password_changed":{
        "model_name":"SampleFormHasParameter",
        "path":frontend_setting.analyst_sample_request_details,
        "admin_message":"A new Sample ({sample_lab_id}) has been assigned for testing",
        "user_message":"None",
    },
    "product_shipped!":{
        "model_name":"SampleFormVerifier",
        "path":frontend_setting.verifier_sample_request_details,
        "admin_message":"A sample report of  ({sample_lab_id}) has been submitted for verification. Please Verify",
        "user_message":"None",
    },
    "new_discount_available!":{
        "model_name":"SampleFormVerifier",
        "path":frontend_setting.admin_sample_request_details,
        "admin_message":"A sample report of  ({sample_lab_id}) has been submitted for approve",
        "user_message":"this sample form verified",
    },
    "product_cancelled!":{
        "model_name":"SampleFormVerifier",
        "path":frontend_setting.sample_request,
        "admin_message":"A sample report of ({sample_lab_id}) has been completed",
        "user_message":"this sample form verified",
    }

}
