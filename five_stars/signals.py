# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from five_stars.models import CustomUser
#
#
# @receiver(post_save, sender=CustomUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:  # This means the user was just created (registered)
#         subject = 'Welcome to Our Site'
#         message = f'Hi {instance.username}, thank you for registering at our site.'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]
#
#         # Send the email
#         send_mail(subject, message, from_email, recipient_list)
