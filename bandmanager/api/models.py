from django.db import models
import uuid

# Create your models here.
class Person(models.Model):
    # - uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    first_name = models.TextField()
    last_name = models.TextField()
    # - address
    address = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zip = models.TextField(null=True)
    country = models.TextField(null=True)
    # - phone
    phone = models.TextField(null=True)
    # - email
    email = models.EmailField(null=True)
    # - is a youth member
    youth = models.BooleanField(null=True)
    # - headshot (including size and quality requirements)
    headshot_url = models.URLField(null=True)
    # - social - either store a JSON object or link to a mapping table
    social_media_info = models.JSONField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
    name = models.TextField(null=True)
    #- abbreviation
    abbreviation = models.TextField(null=True)
    # bands
    def __str__(self):
        return f"{self.name}"

class Band(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- many musicians - handled on musician object
    #- one-n director - handled on director object
    #- address
    address = models.TextField(null=True)
    #- social - either store a JSON object or link to a mapping table
    social_media_info = models.JSONField(null=True)
    #- contact (person ID foreign key)
    contact = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    #- one-n section mapping
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, null=True)
    #- band photo (including size and quality requirements)
    band_photo_url = models.URLField(null=True)
    #- band logo (including size and quality)
    band_logo_url = models.URLField(null=True)
    #- band bio
    band_bio = models.TextField(null=True)
    name = models.TextField(default="")

    def __str__(self):
        return f"{self.name}"

class Venue(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- venue name
    name = models.TextField(null=True)
    #- address
    address = models.TextField(null=True)
    #- venue information
    venue_information = models.TextField(null=True)
    #- map
    map_url = models.URLField(null=True)

    image_url = models.URLField(null=True)

    website = models.URLField(null=True)

    def __str__(self):
        return f"{self.name}"
    

class Contest(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- name
    name = models.TextField(null=True)
    #- contest_year
    date = models.DateField(null=True)
    #- timestamp

    #- lsit of bands
    bands = models.ManyToManyField(Band)
    # performance venue
    venue = models.ForeignKey(Venue, on_delete=models.DO_NOTHING, null=True)
    judge_bio_link = models.URLField(null=True)
    solo_ensemble_link = models.URLField(null=True)
    #- list of performance slots - done through performance slots
    def __str__(self):
        return f"{self.name}"


class Musician(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- person ID
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    #- Instrument association
    instrument = models.TextField(null=True)
    #- list of band affiliations
    bands = models.ManyToManyField(Band)

    def __str__(self):
        return f"{self.person}"

class Director(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    # - Person ID
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    # - bio
    bio = models.TextField(null=True)
    # bands
    bands = models.ManyToManyField(Band)

    def __str__(self):
        return f"{self.person.first_name} + {self.person.last_name} - {','.join(band.name for band in self.bands)}"


class Music(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- test piece flag
    is_test_piece = models.BooleanField(default=False)
    #- section association (only for test pieces)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, null=True)
    #- publisher
    publisher = models.TextField(null=True)
    #- title
    title = models.TextField(null=True)
    #- composer
    composer = models.TextField(null=True)
    #- performance length
    performance_length = models.TextField(null=True)
    #- reference recording link
    reference_recording_url = models.URLField(null=True)
    
    def __str__(self):
        return f"{self.title} ({self.composer})"
    

class PerformanceSlot(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- band ID (null for solo/ensemble contest)
    band = models.ForeignKey(Band, on_delete=models.DO_NOTHING, null=True)
    #- contest ID
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING, null=True)
    #- individual ID (null for band contest)
    person = models.ForeignKey(Person, null=True, on_delete=models.DO_NOTHING)
    #- master_start_time - the absolute earliest obligation imposed on a band member by this performance slot assignment
    master_start_time = models.DateTimeField(null=True)
    #- master_end_time - the absolute latest time all obligations for this slot have been completed
    master_end_time = models.DateTimeField(null=True)
    #- performance timestamp
    performance_time = models.DateTimeField(null=True)
    performance_end_time = models.DateTimeField(null=True)
    stage = models.TextField(null=True)
    #- slot designation (i.e. AA, BB, etc)
    slot_anonymizing_slug = models.TextField(null=True)
    #- venue
    venue = models.ForeignKey(Venue, on_delete=models.DO_NOTHING, null=True)
    #- youtube or other video link
    streaming_links = models.JSONField(null=True)
    #- warmup room
    warmup_location = models.TextField(null=True)
    #- case storage
    case_storage = models.TextField(null=True)
    #- warmup timestamp
    warmup_time = models.DateTimeField(null=True)
    #- photo timestamp
    photo_time = models.DateTimeField(null=True)
    
    music = models.ManyToManyField(Music, null=True)

    title = models.TextField(null=True)
    description = models.TextField(null=True)
    slot_image = models.URLField(null=True) # URL to image of the slot
    #- 1 to N list of judge IDs - handled on judges
    def __str__(self):
        return f"{self.performance_time}"

class Ensemble(models.Model):
    #- uuid
    uuid = models.UUIDField(default=uuid.uuid4)
    #- name
    name = models.TextField(null=True)
    #- one-n musician mapping
    members = models.ManyToManyField(Musician)

    def __str__(self):
        return f"{self.name}"

class Judge(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- person UUID
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    #- bio
    bio = models.TextField(null=True)
    #- headshot
    headshot_url = models.URLField(null=True)
    slots = models.ManyToManyField(PerformanceSlot)

    def __str__(self):
        return f"{self.person}"

class Volunteer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- slot_id
    slot = models.ForeignKey(PerformanceSlot, on_delete=models.DO_NOTHING, null=True)
    #- contest_id
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING, null=True)
    #- person_id
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.person}"


# sections represented as CURRENT_CONTEST_SECTION -- NABBA_SECTION when presented



class Purchases(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- person uuid
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    #- stripe uuid
    stripe_uuid = models.TextField(null=True)
    #- creation date
    creation_date = models.DateTimeField(null=True)
    #- expiry date (for subscriptions only, nullable for one-off purchases)
    expiry_date = models.DateTimeField(null=True)
    #- is a subscription
    is_subscription = models.BooleanField(default=False)
    #- description (hoodie, lifetime member, whatever else)
    description = models.TextField(null=True)

class Score(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- link to score sheet
    score_sheet_url = models.URLField(null=True)
    #- link to band
    band = models.ForeignKey(Band, on_delete=models.DO_NOTHING, null=True)
    #- link to contest
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING, null=True)
    score = models.FloatField(null=True)

class Commentary(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    #- link to commentary file (competition suite?)
    commentary_url = models.URLField(null=True)
    #- link to performance slot
    performance_slot = models.ForeignKey(PerformanceSlot, on_delete=models.DO_NOTHING, null=True)


class Partner(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    image_src = models.URLField(null=True)
    name = models.TextField(null=True)
    link = models.URLField(null=True)
    background = models.TextField(null=True)
    contest = models.ForeignKey(Contest, on_delete=models.DO_NOTHING, null=True)