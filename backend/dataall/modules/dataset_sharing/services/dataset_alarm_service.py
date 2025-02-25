import logging
from datetime import datetime

from dataall.core.environment.db.environment_models import Environment
from dataall.modules.dataset_sharing.db.share_object_models import ShareObject
from dataall.modules.datasets_base.db.dataset_models import DatasetTable, Dataset, DatasetStorageLocation
from dataall.base.utils.alarm_service import AlarmService

log = logging.getLogger(__name__)


class DatasetAlarmService(AlarmService):
    """Contains set of alarms for datasets"""

    def trigger_table_sharing_failure_alarm(
            self,
            table: DatasetTable,
            share: ShareObject,
            target_environment: Environment,
    ):
        log.info('Triggering share failure alarm...')
        subject = (
            f'ALARM: DATAALL Table {table.GlueTableName} Sharing Failure Notification'
        )
        message = f"""
    You are receiving this email because your DATAALL {self.envname} environment in the {self.region} region has entered the ALARM state, because it failed to share the table {table.GlueTableName} with Lake Formation.

    Alarm Details:
        - State Change:               	OK -> ALARM
        - Reason for State Change:      Lake Formation sharing failure
        - Timestamp:                              {datetime.now()}

        Share Source
        - Dataset URI:                   {share.datasetUri}
        - AWS Account:                {table.AWSAccountId}
        - Region:                            {table.region}
        - Glue Database:              {table.GlueDatabaseName}
        - Glue Table:                     {table.GlueTableName}

        Share Target
        - AWS Account:                {target_environment.AwsAccountId}
        - Region:                            {target_environment.region}
        - Glue Database:              {table.GlueDatabaseName}shared
    """
        return self.publish_message_to_alarms_topic(subject, message)

    def trigger_revoke_table_sharing_failure_alarm(
            self,
            table: DatasetTable,
            share: ShareObject,
            target_environment: Environment,
    ):
        log.info('Triggering share failure alarm...')
        subject = f'ALARM: DATAALL Table {table.GlueTableName} Revoking LF permissions Failure Notification'
        message = f"""
    You are receiving this email because your DATAALL {self.envname} environment in the {self.region} region has entered the ALARM state, because it failed to revoke Lake Formation permissions for table {table.GlueTableName} with Lake Formation.

    Alarm Details:
        - State Change:               	OK -> ALARM
        - Reason for State Change:      Lake Formation sharing failure
        - Timestamp:                              {datetime.now()}

        Share Source
        - Dataset URI:                   {share.datasetUri}
        - AWS Account:                {table.AWSAccountId}
        - Region:                            {table.region}
        - Glue Database:              {table.GlueDatabaseName}
        - Glue Table:                     {table.GlueTableName}

        Share Target
        - AWS Account:                {target_environment.AwsAccountId}
        - Region:                            {target_environment.region}
        - Glue Database:              {table.GlueDatabaseName}shared
    """
        return self.publish_message_to_alarms_topic(subject, message)

    def trigger_dataset_sync_failure_alarm(self, dataset: Dataset, error: str):
        log.info(f'Triggering dataset {dataset.name} tables sync failure alarm...')
        subject = (
            f'ALARM: DATAALL Dataset {dataset.name} Tables Sync Failure Notification'
        )
        message = f"""
You are receiving this email because your DATAALL {self.envname} environment in the {self.region} region has entered the ALARM state, because it failed to synchronize Dataset {dataset.name} tables from AWS Glue to the Search Catalog.

Alarm Details:
    - State Change:               	OK -> ALARM
    - Reason for State Change:      {error}
    - Timestamp:                              {datetime.now()}
    Dataset
     - Dataset URI:                   {dataset.datasetUri}
     - AWS Account:                {dataset.AwsAccountId}
     - Region:                            {dataset.region}
     - Glue Database:              {dataset.GlueDatabaseName}
    """
        return self.publish_message_to_alarms_topic(subject, message)

    def trigger_folder_sharing_failure_alarm(
        self,
        folder: DatasetStorageLocation,
        share: ShareObject,
        target_environment: Environment,
    ):
        log.info('Triggering share failure alarm...')
        subject = (
            f'ALARM: DATAALL Folder {folder.S3Prefix} Sharing Failure Notification'
        )
        message = f"""
You are receiving this email because your DATAALL {self.envname} environment in the {self.region} region has entered the ALARM state, because it failed to share the folder {folder.S3Prefix} with S3 Access Point.
Alarm Details:
    - State Change:               	OK -> ALARM
    - Reason for State Change:      S3 Folder sharing failure
    - Timestamp:                              {datetime.now()}
    Share Source
    - Dataset URI:                   {share.datasetUri}
    - AWS Account:                   {folder.AWSAccountId}
    - Region:                            {folder.region}
    - S3 Bucket:                     {folder.S3BucketName}
    - S3 Folder:                     {folder.S3Prefix}
    Share Target
    - AWS Account:                {target_environment.AwsAccountId}
    - Region:                            {target_environment.region}
"""
        return self.publish_message_to_alarms_topic(subject, message)

    def trigger_revoke_folder_sharing_failure_alarm(
        self,
        folder: DatasetStorageLocation,
        share: ShareObject,
        target_environment: Environment,
    ):
        log.info('Triggering share failure alarm...')
        subject = (
            f'ALARM: DATAALL Folder {folder.S3Prefix} Sharing Revoke Failure Notification'
        )
        message = f"""
You are receiving this email because your DATAALL {self.envname} environment in the {self.region} region has entered the ALARM state, because it failed to share the folder {folder.S3Prefix} with S3 Access Point.
Alarm Details:
    - State Change:               	OK -> ALARM
    - Reason for State Change:      S3 Folder sharing Revoke failure
    - Timestamp:                              {datetime.now()}
    Share Source
    - Dataset URI:                   {share.datasetUri}
    - AWS Account:                   {folder.AWSAccountId}
    - Region:                            {folder.region}
    - S3 Bucket:                     {folder.S3BucketName}
    - S3 Folder:                     {folder.S3Prefix}
    Share Target
    - AWS Account:                {target_environment.AwsAccountId}
    - Region:                            {target_environment.region}
"""
        return self.publish_message_to_alarms_topic(subject, message)
