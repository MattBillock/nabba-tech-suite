from django.db import models
import uuid

# Create your models here.
class Person(models.Model):
    # - uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    # - address
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()
    country = models.TextField()
    # - phone
    phone = models.TextField()
    # - email
    email = models.EmailField()
    # - is a youth member
    youth = models.BooleanField()
    # - headshot (including size and quality requirements)
    headshot_url = models.URLField()
    # - social - either store a JSON object or link to a mapping table
    social_media_info = models.JSONField()

class EmailPreference(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    bridge_flag = models.BooleanField(default=True)
    contest_flag = models.BooleanField(default=True)
    general_flag = models.BooleanField(default=True)


class Section(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- uuid
    #- name
    name = models.TextField()
    #- abbreviation
    abbreviation = models.TextField()
    # bands

class Band(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- many musicians - handled on musician object
    #- one-n director - handled on director object
    #- address
    address = models.TextField()
    #- social - either store a JSON object or link to a mapping table
    social_media_info = models.JSONField()
    #- contact (person ID foreign key)
    contact = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    #- one-n section mapping
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    #- band photo (including size and quality requirements)
    band_photo_url = models.URLField()
    #- band logo (including size and quality)
    band_logo_url = models.URLField()
    #- band bio
    band_bio = models.TextField()


class Contest(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- name
    name = models.TextField()
    #- contest_year
    date = models.DateField()
    #- timestamp

    #- lsit of bands
    bands = models.ManyToManyField(Band)
    #- list of performance slots - done through performance slots






class Musician(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- person ID
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    #- Instrument association
    instrument = models.TextField()
    #- list of band affiliations
    bands = models.ManyToManyField(Band)

class Director(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    # - Person ID
    person = models.OneToOneField(Person, on_delete=models.DO_NOTHING)
    # - bio
    bio = models.TextField()
    # bands
    bands = models.ManyToManyField(Band)



class Venue(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- venue name
    name = models.TextField()
    #- address
    address = models.TextField()
    #- venue information
    venue_information = models.TextField()
    #- map
    map_url = models.URLField()


class PerformanceSlot(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- band ID (null for solo/ensemble contest)
    band = models.ForeignKey(Band, on_delete=models.DO_NOTHING)
    #- contest ID
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING)
    #- individual ID (null for band contest)
    person = models.ForeignKey(Person, null=True, on_delete=models.DO_NOTHING)
    #- master_start_time - the absolute earliest obligation imposed on a band member by this performance slot assignment
    master_start_time = models.DateTimeField()
    #- master_end_time - the absolute latest time all obligations for this slot have been completed
    master_end_time = models.DateTimeField()
    #- performance timestamp
    performance_time = models.DateTimeField()
    #- slot designation (i.e. AA, BB, etc)
    slot_anonymizing_slug = models.TextField()
    #- venue
    venue = models.ForeignKey(Venue, on_delete=models.DO_NOTHING)
    #- youtube or other video link
    streaming_links = models.JSONField()
    #- warmup room
    warmup_location = models.TextField()
    #- case storage
    case_storage = models.TextField()
    #- warmup timestamp
    warmup_time = models.DateTimeField()
    #- photo timestamp
    photo_time = models.DateTimeField()
    #- 1 to N list of judge IDs - handled on judges

class Ensemble(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- name
    name = models.TextField()
    #- one-n musician mapping
    members = models.ManyToManyField(Musician)

class Judge(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- person UUID
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    #- bio
    bio = models.TextField()
    #- headshot
    headshot_url = models.URLField()
    slots = models.ManyToManyField(PerformanceSlot)

class Volunteer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- slot_id
    slot = models.ForeignKey(PerformanceSlot, on_delete=models.DO_NOTHING)
    #- contest_id
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING)
    #- person_id
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)



# sections represented as CURRENT_CONTEST_SECTION -- NABBA_SECTION when presented


class Music(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- test piece flag
    is_test_piece = models.BooleanField(default=False)
    #- section association (only for test pieces)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    #- publisher
    publisher = models.TextField()
    #- title
    title = models.TextField()
    #- composer
    composer = models.TextField()
    #- performance length
    performance_length = models.TextField()
    #- reference recording link
    reference_recording_url = models.URLField()

class Purchases(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- person uuid
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    #- stripe uuid
    stripe_uuid = models.TextField()
    #- creation date
    creation_date = models.DateTimeField()
    #- expiry date (for subscriptions only, nullable for one-off purchases)
    expiry_date = models.DateTimeField()
    #- is a subscription
    is_subscription = models.BooleanField(default=False)
    #- description (hoodie, lifetime member, whatever else)
    description = models.TextField()

class Score(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- link to score sheet
    score_sheet_url = models.URLField()
    #- link to band
    band = models.ForeignKey(Band, on_delete=models.DO_NOTHING)
    #- link to contest
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING)
    score = models.FloatField()

class Commentary(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- link to commentary file (competition suite?)
    commentary_url = models.URLField()
    #- link to performance slot
    performance_slot = models.ForeignKey(PerformanceSlot, on_delete=models.DO_NOTHING)
