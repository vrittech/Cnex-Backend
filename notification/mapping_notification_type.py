from . import frontend_setting
mapping = {
    "service_booked":{
        "model_name":"Appointment",
        "admin_message":"",
        "path":"appointments",
        "admin_message":"Your {services_name} service has been successfully booked through our app. We'll keep you updated every step of the way.",
        "user_message":"Your {services_name} service has been successfully booked through our app. We'll keep you updated every step of the way.",
    },
    "payment_confirmed":{
        "model_name":"Order",
        "path":"orderDetails/:{order_id}",
        "admin_message":"Your payment of Order ID {order_id} has been successfully confirmed. Thank you for your purchase!",
        "user_message":"Your payment of Order ID {order_id} has been successfully confirmed. Thank you for your purchase!",
    },
    "password_changed":{
        "model_name":"CustomUser",
        "path":"notifications",
        "admin_message":"Your password has been changed successfully. Remember to keep it secure!",
        "user_message":"Your password has been changed successfully. Remember to keep it secure!",
    },
    "order_shipped":{
        "model_name":"Order",
        "path":"orderDetails/{order_id}",
        "admin_message":"Your ordered product {order_id} has been delivered to your doorstep. Enjoy your purchase!",
        "user_message":"Your ordered product {order_id} has been delivered to your doorstep. Enjoy your purchase!",
    },
    "order_delivered":{
        "model_name":"Order",
        "path":"orderDetails/{order_id}",
        "admin_message":"Your ordered product {order_id} has been delivered to your doorstep. Enjoy your purchase!",
        "user_message":"Your ordered product {order_id} has been delivered to your doorstep. Enjoy your purchase!",
    },
    "order_cancelled":{
        "model_name":"Order",
        "path":"orderDetails/{order_id}",
        "admin_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
        "user_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
    },
    "new_coupon":{
        "model_name":"Coupon",
        "path":"coupon",
        "admin_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
        "user_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
    },
    "product_push_notification":{
        "model_name":"Product",
        "path":"products/{slug}",
        "admin_message":"",
        "user_message":"",
    },
       "static_push_notification":{
        "model_name":"Product",
        "path":"/notification",
        "admin_message":"",
        "user_message":"",
    },
       "collection_push_notification":{
        "model_name":"Product",
        "path":"collection/{id}",
        "admin_message":"",
        "user_message":"",
    },
}