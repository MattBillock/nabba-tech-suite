from rest_framework import serializers

from .models import Person, EmailPreference, Section, Band, Commentary, Volunteer, Score, Music, \
        Score, Purchases, Venue, PerformanceSlot, Judge, Contest, Musician, Director, Ensemble, Partner


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Music
        fields = (
            'id',
            'uuid',
            #- test piece flag
            'is_test_piece',
            #- section association (only for test pieces)
            'section',
            #- publisher
            'publisher',
            #- title
            'title',
            #- composer
            'composer',
            #- performance length
            'performance_length',
            #- reference recording link
            'reference_recording_url'
        )

# Create your models here.
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id','uuid', 'first_name', 'last_name', 'address', 'city', 'state', 'zip','country','phone','email','youth','headshot_url', 'social_media_info')

    def __init__(self, *args, **kwargs):
        # Remove unwanted fields
        fields = kwargs.pop('fields', None)
        super(PersonSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    

class EmailPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailPreference
        fields=(
            'id',
            'uuid',
            'person',
            'bridge_flag',
            'contest_flag',
            'general_flag'
        )
    


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields=(
            'id',
            'uuid',
            'name',
            'abbreviation'
        )

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Band
        fields=(
            'id',
            'uuid',
            'name',
            'address',
            'social_media_info',
            'contact',
            'section',
            'band_photo_url',
            'band_logo_url',
            'band_bio'

        )
    
    def __init__(self, *args, **kwargs):
        # Remove unwanted fields
        fields = kwargs.pop('fields', None)
        super(BandSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contest
        fields = (
            'id',
            'uuid',
            'name',
            'date',
            'bands',
            'venue',
            'judge_bio_link',
            'solo_ensemble_link',
            'venue'
        )






class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model=Musician
        fields = (
            'id',
            'uuid',
            'person',
            'instrument',
            'bands'
        )

class DirectorSerializer(serializers.ModelSerializer):
    # bands = serializers.RelatedField(source='bands')

    #bands = BandSerializer(many=True)
    #person = PersonSerializer(fields=['first_name', 'last_name'])
    class Meta:
        model=Director
        fields = (
            'id',
            'uuid',
            'person',
            'bio',
            'bands'
        )



class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Venue
        fields = (
            'id',
            'uuid',
            'name',
            'address',
            'venue_information',
            'map_url',
            'image_url',
            'website',
        )


class PerformanceSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model=PerformanceSlot
        fields = (
            'id',
            'uuid',
            'band',
            'contest',
            'person',
            'master_start_time',
            'master_end_time',
            'performance_time',
            'performance_end_time',
            'stage',
            'slot_anonymizing_slug',
            'venue',
            'streaming_links',
            'warmup_location',
            'case_storage',
            'warmup_time',
            'photo_time',
            'music',
            'title',
            'description',
            'slot_image',
        )
        

class EnsembleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ensemble
        fields = (
            'id',
            #- uuid
            'uuid',
            #- name
            'name',
            #- one-n musician mapping
            'members',
        )

class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Judge
        fields = (
            'id',
            'uuid',
            #- person UUID
            'person',
            #- bio
            'bio',
            #- headshot
            'headshot_url',
            'slots'
        )

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Volunteer
        fields = (
            'id',
            'uuid',
            'slot',
            'contest',
            'person'
        )



# sections represented as CURRENT_CONTEST_SECTION -- NABBA_SECTION when presented



class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchases
        fields = (
            'id',
            'uuid',
            #- person uuid
            'person',
            #- stripe uuid
            'stripe_uuid',
            #- creation date
            'creation_date',
            #- expiry date (for subscriptions only, nullable for one-off purchases)
            'expiry_date',
            #- is a subscription
            'is_subscription',
            #- description (hoodie, lifetime member, whatever else)
            'description'
        )

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Score
        fields = (
            'id',
            'uuid',
            #- link to score sheet
            'score_sheet_url',
            #- link to band
            'band',
            #- link to contest
            'contest',
            'score'
        )

class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model=Commentary
        fields = (
            'id',
            'uuid',
            #- link to commentary file (competition suite?)
            'commentary_url',
            #- link to performance slot
            'performance_slot'
        )
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Partner
        fields = (
            'id',
            'uuid',
            'name',
            'image_src',
            'link',
            'background',
            'contest'
        )