from rest_framework import serializers

from .models import Person, EmailPreference, Section, Band, Commentary, Volunteer, Score, Music, \
        Score, Purchases, Venue, PerformanceSlot, Judge, Contest, Musician, Director, Ensemble

# Create your models here.
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('uuid', 'address', 'city', 'state', 'zip','country','phone','email','youth','headshot_url', 'social_media_info')
    

class EmailPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailPreference
        fields=(
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
            'uuid',
            'name',
            'abbreviation'
        )

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Band
        fields=(
            'uuid',
            'address',
            'social_media_info',
            'contact',
            'section',
            'band_photo_url',
            'band_logo_url',
            'band_bio'

        )
    

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contest
        fields = (
            'uuid',
            'name',
            'date',
            'bands',
        )






class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model=Musician
        fields = (
            'uuid',
            'person',
            'instrument',
            'bands'
        )

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Director
        fields = (
            'uuid',
            'person',
            'bio',
            'bands'
        )



class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Venue
        fields = (
            'uuid',
            'name',
            'address',
            'venue_information',
            'map_url'
        )


class PerformanceSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model=PerformanceSlot
        fields = (
            'uuid',
            'band',
            'contest',
            'person',
            'master_start_time',
            'master_end_time',
            'performance_time',
            'slot_anonymizing_slug',
            'venue',
            'streaming_links',
            'warmup_location',
            'case_storage',
            'warmup_time',
            'photo_time'
        )

class EnsembleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ensemble
        fields = (
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
            'uuid',
            'slot',
            'contest',
            'person'
        )



# sections represented as CURRENT_CONTEST_SECTION -- NABBA_SECTION when presented


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Music
        fields = (
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

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchases
        fields = (
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
            'uuid',
            #- link to commentary file (competition suite?)
            'commentary_url',
            #- link to performance slot
            'performance_slot'
        )
