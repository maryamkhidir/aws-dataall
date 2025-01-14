from dataall.core.notifications.db.notification_repositories import Notification
from dataall.core.notifications.db.notification_models import NotificationType
from dataall.modules.dataset_sharing.db.share_object_models import ShareObject
from dataall.modules.datasets_base.db.dataset_models import Dataset


class ShareNotificationService:
    @staticmethod
    def notify_share_object_submission(
            session, username: str, dataset: Dataset, share: ShareObject
    ):
        notifications = [Notification.create(
            session=session,
            username=dataset.owner,
            notification_type=NotificationType.SHARE_OBJECT_SUBMITTED,
            target_uri=f'{share.shareUri}|{dataset.datasetUri}',
            message=f'User {username} submitted share request for dataset {dataset.label}',
        )]
        session.add_all(notifications)
        return notifications

    @staticmethod
    def notify_share_object_approval(
            session, username: str, dataset: Dataset, share: ShareObject
    ):
        notifications = []
        targeted_users = ShareNotificationService._get_share_object_targeted_users(
            session, dataset, share
        )
        for user in targeted_users:
            notifications.append(
                Notification.create(
                    session=session,
                    username=user,
                    notification_type=NotificationType.SHARE_OBJECT_APPROVED,
                    target_uri=f'{share.shareUri}|{dataset.datasetUri}',
                    message=f'User {username} approved share request for dataset {dataset.label}',
                )
            )
            session.add_all(notifications)
        return notifications

    @staticmethod
    def notify_share_object_rejection(
            session, username: str, dataset: Dataset, share: ShareObject
    ):
        notifications = []
        targeted_users = ShareNotificationService._get_share_object_targeted_users(
            session, dataset, share
        )
        for user in targeted_users:
            notifications.append(
                Notification.create(
                    session=session,
                    username=user,
                    notification_type=NotificationType.SHARE_OBJECT_REJECTED,
                    target_uri=f'{share.shareUri}|{dataset.datasetUri}',
                    message=f'User {username} rejected share request for dataset {dataset.label}',
                )
            )
            session.add_all(notifications)
        return notifications

    @staticmethod
    def notify_new_data_available_from_owners(
            session, dataset: Dataset, share: ShareObject, s3_prefix
    ):
        notifications = []
        targeted_users = ShareNotificationService._get_share_object_targeted_users(
            session, dataset, share
        )
        for user in targeted_users:
            notifications.append(
                Notification.create(
                    session=session,
                    username=user,
                    notification_type=NotificationType.DATASET_VERSION,
                    target_uri=f'{share.shareUri}|{dataset.datasetUri}',
                    message=f'New data (at {s3_prefix}) is available from dataset {dataset.datasetUri} '
                            f'shared by owner {dataset.owner}',
                )
            )
            session.add_all(notifications)
        return notifications

    @staticmethod
    def _get_share_object_targeted_users(session, dataset, share):
        targeted_users = ShareNotificationService._get_dataset_stewards(dataset)
        targeted_users.append(dataset.owner)
        targeted_users.append(share.owner)
        return targeted_users

    @staticmethod
    def _get_dataset_stewards(dataset):
        stewards = list()
        stewards.append(dataset.SamlAdminGroupName)
        stewards.append(dataset.stewards)
        return stewards
