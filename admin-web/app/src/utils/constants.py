# -*- coding: utf-8 -*-

API_BASE_URL = 'http://api.r2s.tirsolutions.com/resources-to-share/api'
#staging
CHAT_SUPPORT_URL = 'http://chat.r2s.tirsolutions.com'

#Live
#CHAT_SUPPORT_URL = 'http://chat.resourcestoshare.com'
IMG_BASE_URL = "http://admin.r2s.tirsolutions.com"
# IMG_BASE_URL = "https://s3-ap-southeast-1.amazonaws.com/resourcestoshare"
# API_BASE_URL = 'http://stagingapi.r2s.tirsolutions.com/resources-to-share-stg/api'

IMAGE_UPLOAD_DIR =  IMG_BASE_URL + '/static/uploads/'

# Analytics
ANALYTICS_ALL = API_BASE_URL + '/admin/analytics'

# Categories
CATEGORIES_ALL = API_BASE_URL + '/categories'
CATEGORIES_ONE = API_BASE_URL + '/categories/{category_id}'
CATEGORIES_RESTORE = API_BASE_URL + '/categories/{category_id}/restore'
CATEGORIES_ACCEPT = API_BASE_URL + '/categories/{category_id}/accept'
CATEGORIES_REJECT = API_BASE_URL + '/categories/{category_id}/reject'


# Sub-Categories
SUBCATEGORIES_ALL = API_BASE_URL + '/categories/{category_id}/subcategories'
SUBCATEGORIES_ONE = API_BASE_URL + '/categories/{category_id}/subcategories/{subcategory_id}'
SUBCATEGORIES_RESTORE = API_BASE_URL + '/categories/{category_id}/subcategories/{subcategory_id}/restore'
SUBCATEGORIES_ACCEPT = API_BASE_URL + '/categories/{category_id}/subcategories/{subcategory_id}/accept'
SUBCATEGORIES_REJECT = API_BASE_URL + '/categories/{category_id}/subcategories/{subcategory_id}/reject'


# Suggested Category
SUGGESTED_CATEGORY_ACCEPT = API_BASE_URL + '/categories/{suggested_category_id}/accept'
SUGGESTED_CATEGORY_REJECT = API_BASE_URL + '/categories/{suggested_category_id}/reject'


# Suggested Subcategories
SUGGESTED_SUBCATEGORY_ACCEPT = API_BASE_URL + '/categories/{suggested_category_id}/subcategories/{suggested_subcategory_id}/accept'
SUGGESTED_SUBCATEGORY_REJECT = API_BASE_URL + '/categories/{suggested_category_id}/subcategories/{suggested_subcategory_id}/reject'


# Admin Functionalities
USER_BAN = API_BASE_URL + '/users/{user_id}/ban'
USER_DEACTIVATE = API_BASE_URL + '/users/{user_id}'
USER_RESTORE = API_BASE_URL + '/users/{user_id}/restore'
USER_RESEND = API_BASE_URL + '/users/resend/email'


# Admin Users
ADMIN_ALL = API_BASE_URL + '/admin/users'
ADMIN_ONE = API_BASE_URL + '/admin/users/{username}'
ADMIN_RESTORE = API_BASE_URL + '/admin/users/{username}/restore'
ADMIN_CHANGE = API_BASE_URL + '/admin/users/{username}/password'


# Users
USERT_ALL = API_BASE_URL + '/users'
USERS_ONE = API_BASE_URL + '/users/{user_id}'
USER_LOGIN = API_BASE_URL + '/admin/users/login'
USER_REGISTER = API_BASE_URL + '/users/register'
USER_PASSWORD = API_BASE_URL + '/users/{user_id}/password'
USER_RESOURCE_ALL = API_BASE_URL + '/users/{user_id}/resources'
USER_RESOURCE_ONE = API_BASE_URL + '/users/{user_id}/resources/{resource_id}'
USER_RESOURCE_RESTORE = API_BASE_URL + '/users/{user_id}/resources/{resource_id}/restore'
USER_FAVORITE = API_BASE_URL + '/users/{user_id}/resources/favorites'
USER_TRANSACTIONS = API_BASE_URL + '/users/{user_id}/transactions'
USER_TRANSACTION_DETAIL = API_BASE_URL + '/users/{user_id}/transactions/{transaction_id}'
USER_TRANSACTIONS_SELLING = API_BASE_URL + '/users/{user_id}/transactions/selling'
USER_TRANSACTIONS_BUYING = API_BASE_URL + '/users/{user_id}/transactions/buying'
USER_TRANSACTION_RATE = API_BASE_URL + '/users/{user_id}/transactions/{transaction_id}/rate'


# FAQS
FAQ_ALL = API_BASE_URL + '/faqs'
FAQ_ONE = API_BASE_URL + '/faqs/{faq_id}'
FAQ_RESTORE = API_BASE_URL + '/faqs/{faq_id}/restore'


# Questions
FAQ_QUESTION_ALL = API_BASE_URL + '/faqs/{faq_id}/questions'
FAQ_QUESTION_ONE = API_BASE_URL + '/faqs/{faq_id}/questions/{question_id}'
FAQ_QUESTION_RESTORE = API_BASE_URL + '/faqs/{faq_id}/questions/{question_id}/restore'
FAQ_ARRANGE = API_BASE_URL + '/faqs/arrange'
QUESTIONS_ARRANGE = API_BASE_URL + '/faqs/arrange?categoryId={faq_id}'



# Resources
RESOURCE_ALL = API_BASE_URL + '/resources'
RESOURCE_ONE = API_BASE_URL + '/resources/{resource_id}'
RESOURCE_BAN = API_BASE_URL + '/resources/{resource_id}/ban'
RESOURCE_ACCEPT = API_BASE_URL + '/resources/{resource_id}/accept'
RESOURCE_REJECT = API_BASE_URL + '/resources/{resource_id}/reject'
RESOURCE_RESTORE = API_BASE_URL + '/resources/{resource_id}/restore'
RESOURCE_UPDATE = API_BASE_URL + '/resources/{resource_id}/updates'
RESOURCE_KEYWORD = API_BASE_URL + '/new/resources/{resource_id}'


# Update Resources
# UPDATED_ONE = API_BASE_URL + '/resources/{update_id}/updates'
UPDATED_ONE = API_BASE_URL + '/new/resources/{update_id}'
UPDATED_ACCEPT = API_BASE_URL + '/resources/{update_id}/updates/{snapshot_code}'
UPDATED_REJECT = API_BASE_URL + '/resources/{update_id}/updates/{snapshot_code}'


# Companies
COMPANIES_ALL = API_BASE_URL + '/companies'
# COMPANIES_ALL = API_BASE_URL + '/companies?limit=1000'
COMPANIES_ONE = API_BASE_URL + '/companies/{company_id}'
COMPANIES_RESTORE = API_BASE_URL + '/companies/{company_id}/restore'


# Support Ticket Requests
TICKET_ALL = API_BASE_URL + '/support/requests'
TICKET_ONE = API_BASE_URL + '/support/requests/{ticket_id}'
TICKET_ACCEPT = API_BASE_URL + '/support/requests/{ticket_id}'
TICKET_CLOSE = API_BASE_URL + '/support/requests/{ticket_id}/closed'


# Banners
BANNER_ALL = API_BASE_URL + '/ads'
BANNER_ONE = API_BASE_URL + '/ads/{banner_id}'
BANNER_RESTORE = API_BASE_URL + '/ads/{banner_id}/restore'


# Images
BANNER_IMAGE_ALL = API_BASE_URL + '/ads/{banner_id}/images'
BANNER_IMAGE_ONE = API_BASE_URL + '/ads/{banner_id}/images/{image_id}'
BANNER_IMAGE_RESTORE = API_BASE_URL + '/ads/{banner_id}/images/{image_id}/restore'


# Wishlists
WISHLIST_ALL = API_BASE_URL + '/wishlists'
WISHLIST_ONE = API_BASE_URL + '/wishlists/{wishlist_id}'
WISHLIST_ACCEPT = API_BASE_URL + '/wishlists/{wishlist_id}/accept'
WISHLIST_REJECT = API_BASE_URL + '/wishlists/{wishlist_id}/reject'
WISHLIST_RESTORE = API_BASE_URL + '/wishlists/{wishlist_id}/restore'


#Invitation
INVITE_USERS = API_BASE_URL + '/admin/users/invite'


#chat
ADMIN_SUPPORT_REQUEST = CHAT_SUPPORT_URL + '/admin/supportrequests'
ADMIN_SUPPORT_REQUEST_CREATE = CHAT_SUPPORT_URL + '/admin/supportrequests/create'
ADMIN_SUPPORT_REQUEST_PROFILE = CHAT_SUPPORT_URL + '/admin/supportrequests/{reference_code}/profile'
ADMIN_SUPPORT_CONVERSATION = CHAT_SUPPORT_URL + '/admin/supportrequests/conversation'
ADMIN_SUPPORT_CHAT_STATUS = CHAT_SUPPORT_URL + '/admin/supportrequests/status'

#Inviation
INVITATION_ADD_EMAIL = CHAT_SUPPORT_URL + '/v2/contacts'
INVITATION_REMOVED_EMAIL = CHAT_SUPPORT_URL + '/v2/contacts/{email_category}/admin/1'
# Image Upload
IMAGE_UPLOAD = API_BASE_URL + '/upload/images'
