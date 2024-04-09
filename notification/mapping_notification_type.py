from . import frontend_setting
mapping = {
    "service_booked":{
        "model_name":"Appointment",
        "admin_message":"",
        "path":"appointments",
        "admin_message":"Your {{service name}} service has been successfully booked through our app. We'll keep you updated every step of the way.",
        "user_message":"Your {{service name}} service has been successfully booked through our app. We'll keep you updated every step of the way.",
    },
    "payment_confirmed":{
        "model_name":"Order",
        "path":"orderDetails/:order_id",
        "admin_message":"Your payment of Order ID {{Order ID}} has been successfully confirmed. Thank you for your purchase!",
        "user_message":"Your payment of Order ID {{Order ID}} has been successfully confirmed. Thank you for your purchase!",
    },
    "password_changed":{
        "model_name":"CustomUser",
        "path":"notifications",
        "admin_message":"Your password has been changed successfully. Remember to keep it secure!",
        "user_message":"Your password has been changed successfully. Remember to keep it secure!",
    },
    "product_shipped!":{
        "model_name":"Order",
        "path":"orderDetails/:order_id",
        "admin_message":"Your ordered product {{Order ID}} has been delivered to your doorstep. Enjoy your purchase!",
        "user_message":"Your ordered product {{Order ID}} has been delivered to your doorstep. Enjoy your purchase!",
    },
    "Product Delivered!":{
        "model_name":"Order",
        "path":"orderDetails/:order_id",
        "admin_message":"Your ordered product {{Order ID}} has been delivered to your doorstep. Enjoy your purchase!",
        "user_message":"Your ordered product {{Order ID}} has been delivered to your doorstep. Enjoy your purchase!",
    },
    "new_discount_available!":{
        "model_name":"Coupon",
        "path":"coupon",
        "admin_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
        "user_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
    },
    "product_cancelled!":{
        "model_name":"Order",
        "path":"orderDetails/:order_id",
        "admin_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
        "user_message":"We're excited to announce a new discount coupon created just for you! Check out the app for exclusive savings.",
    }

}