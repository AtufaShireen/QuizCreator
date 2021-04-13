# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Quizzer,UserTags


# @receiver(post_save, sender=Quizzer)
# def create_profile(sender, instance, created, **kwargs):
#     user=User.objects.get(user=instance.user)
#     if created:
#         UserTags.objects.create(user=user,tags={user.username:instance.tags})


# @receiver(post_save, sender=Quizzer) # for update
# def save_profile(sender, instance, **kwargs):
#     instance.user.Usertags.save()
