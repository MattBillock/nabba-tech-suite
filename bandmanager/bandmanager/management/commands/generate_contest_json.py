from django.core.management.base import BaseCommand, CommandError

from api.models import Contest, Director, PerformanceSlot, Venue
from collections import defaultdict
from datetime import datetime

import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Command(BaseCommand):
    help = 'Builds the contest config file'

    def add_arguments(self, parser):
        # Optional: add arguments here if needed
        parser.add_argument('contest_id', type=int, help='The database ID of the contest for which we are generating the config')

    def build_music_list_for_band(self, band, contest):
        performance_slots = PerformanceSlot.objects.filter(contest=contest, band=band).all()
        return_value = []
        for slot in performance_slots:           
             for piece in slot.music.all():
                return_value.append({
                    "title": piece.title,
                    "composer": piece.composer,
                    "performance_slot": slot.slot_anonymizing_slug
                })
            
        return return_value
    
    def get_draw_identifiers_for_band(self, band, contest):
        return PerformanceSlot.objects.filter(contest=contest, band=band).values_list('slot_anonymizing_slug', flat=True)

    def build_band_list(self, bands, contest):
        """
        {
        "band_list": [
            {
            "id": 1,
            "name": "Chicago Brass Band",
            "website": "https://chicagobrassband.org",
            "band_bio": "The Chicago Brass Band is a 30-piece brass and percussion ensemble formed in the British brass band tradition, but with Chicago flair. The band, led by music director Dr. Mark Taylor, just celebrated its 20th anniversary. During its first two decades, the Chicago Brass Band has won the North American Brass Band Championship, been awarded Most Entertaining Band at the US Open Brass Band Championships, twice competed in the World Music Contest in the Netherlands, participated in the renowned Whit Friday Marches in England, has been a featured ensemble in front of 40,000 brass fans at the Great American Brass Festival, competed in the 2019 New Zealand National Brass Band Championships, and won first prize at the 2019 Gateway British Brass Band Festival. The band’s favorite activity, however, remains dazzling audiences in Chicago, one of the world’s premiere cities for brass musicianship. The band has particularly enjoyed performances with soloists drawn from the Chicago Symphony Orchestra’s celebrated brass section, including Chris Martin, Charlie Vernon, Gene Pokorny, John Hagstrom, and Mark Ridenour, and multiple collaborations with famed artist Rex Richardson. The Chicago Brass Band was selected to be a Chamber Group at the 2011 Midwest Band and Orchestra Clinic in Chicago, with guest soloist Jens Lindemann- rekindling the brass band movement at this annual convention. Additionally, the Chicago Brass Band has continued engaging young musicians with its Project Horizon initiative, a program developed to promote and enhance the performance and enjoyment of live music in public schools. Through collaborative concerts, workshops, and clinics, the band inspires students to continue to perform and enjoy live music at a high level into and throughout adulthood, even if they do not pursue music as their chosen profession.",
            "band_photo": "https://nabba-mobile-app.sfo3.cdn.digitaloceanspaces.com/band_media/1/band_photo.jpg",
            "band_logo": "https://nabba-mobile-app.sfo3.cdn.digitaloceanspaces.com/band_media/1/band_logo.jpg",
            "conductor_name": "Mark Taylor",
            "conductor_bio": "Mark A. Taylor is honored to serve as the new Music Director of the internationally award-winning Chicago Brass Band. Dr. Taylor is a conductor, educator, and performer in demand throughout the Great Lakes region. His new appointment follows nearly twenty years as a section percussionist with the band. No stranger to brass band leadership, Dr. Taylor is now entering his second decade as Music Director of the Milwaukee Festival Brass. He is also the Music Director of the Waukegan Band and serves as Band Director at College of DuPage. He received the Doctor of Musical Arts degree in 2016 from the University of North Texas, where his principal conducting teachers were Eugene Migliaro Corporon, Dennis Fisher, and Nicholas Enrico Williams. Dr. Taylor’s dissertation, 'British-Style Brass Bands in U.S. Colleges and Universities,' documented the existence of brass bands in American college music programs, past and present. Prior to his doctoral study, he served five years as Director of Bands and Coordinator of Ensembles at Loyola University Chicago, and taught on the music education faculty at the Chicago College of Performing Arts at Roosevelt University. He received the Master of Music degree from Northwestern University, where he studied conducting with John P. Paynter and Stephen G. Peterson and music education with Bennett Reimer and Peter Webster. He received his undergraduate degrees from the University of Notre Dame, where his first conducting teachers were Walter Ginter and Carl Stam. Dr. Taylor and his wife and son reside in Lake Forest, IL.",
            "conductor_photo": "https://nabba-mobile-app.sfo3.cdn.digitaloceanspaces.com/band_media/1/conductor_photo.jpg",
            "contact_email": "vicepresident@chicagobrassband.org",
            "choice_pieces": [
                {
                "title": "Titan's Progress",
                "composer": "Hermann Pallhuber",
                "performance_slot": "C_G"
                },
                {
                "title": "A Gabrieli Fantasy",
                "composer": "Bert Appermont",
                "performance_slot": "C_DD"
                }
            ],
            "band_section": "championship",
            "contest_draw_identifiers": ["C_G","C_DD"]
            },
        ],
        """
        print(bands)
        result = []
        
        for band in bands:
            director = Director.objects.filter(bands=band).first()
            result.append({
                "id": 1,
                "name": band.name,
                "website": band.social_media_info.get('website'),
                "band_bio": band.band_bio,
                "band_photo": band.band_photo_url,
                "band_logo": band.band_logo_url,
                "conductor_name": director.person.first_name + ' ' + director.person.last_name,
                "conductor_bio": director.bio,
                "conductor_photo": director.person.headshot_url,
                "contact_email": band.contact.email,
                "choice_pieces": self.build_music_list_for_band(band, contest),
                "band_section": band.section.name,
                "contest_draw_identifiers": list(self.get_draw_identifiers_for_band(band, contest))
            })
        return result
    
    def build_performance_schedule(self, contest):
        """
        "performance_schedule": {
            "2023-04-20": [
            {
                "band_id": 1000,
                "band_draw": "session_1",
                "stage": "Full Schedule",
                "title": "Band and Solo Rehearsals Open",
                "details": "Rehearsals open for those with reserved rehearsal slots",
                "slot_image": "",
                "performance_times": {
                "start_timestamp": "2023-04-20T15:30:00.000-05:00",
                "end_timestamp": "2023-04-20T21:15:00.000-05:00"
                }

            },
            ],
            "2023-04-21": [
                ...
            ],
            "2023-04-22": [
                ...
            ]
        },
        """
        performance_slots_for_contest = PerformanceSlot.objects.filter(contest=contest).all()
        schedule_dict = defaultdict(list)
        for slot in performance_slots_for_contest:
            print(slot)
            schedule_day = slot.performance_time.strftime("%Y-%m-%d")
            band_id = slot.band.id if slot.band else None
            schedule_dict[schedule_day].append({
                "band_id": band_id,
                "band_draw": slot.slot_anonymizing_slug,
                "stage": slot.stage,
                "title": slot.title,
                "details": slot.description,
                "slot_image": slot.slot_image,
                "performance_times": {
                    "start_timestamp": slot.performance_time,
                    "end_timestamp": slot.performance_end_time
                }
            })
        return schedule_dict
    
    def build_venue_details(self, contest):

        """
        "venue_details": {
            "name": "The Von Braun Center",
            "image": "https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,h_640,q_50,w_1280/v1/clients/vonbrauncenter/180810_VBCC_002_X3_1eee8497-7782-4983-9e86-56fb4cee24e8.jpg",
            "address": "700 Monroe Street, Huntsville, Alabama 35801",
            "map_file": "https://goo.gl/maps/cngBNm88WPDD6Xh87",
            "description": "NABBA is proud to once again be hosting the contest at the Von Braun Center. The Von Braun Center, named for rocket pioneer Dr. Wernher Von Braun, is located in the heart of historic downtown Huntsville, Alabama. This multi-purpose facility is equipped to accommodate major conferences, conventions, concerts, Broadway performances, ballets, symphonies, a full range of sporting events and so much more! Huntsville is a high-tech city with a history of Southern hospitality. The VBC is just a short drive from the International Airport and convenient to area hotels. The Von Braun Center is a turn-key facility with a team of experienced professionals ready to guarantee the success of your event.",
            "link": "https://www.vonbrauncenter.com/",
            "contest_name": "North American Brass Band Championships",
            "judge_link": "https://nabba.org/wp-content/uploads/2023/01/2023-NABBC-Band-Judges.pdf",
            "solo_ensemble_link": "https://nabba.org/championships/solo-and-ensemble-schedules/"
        },
        """
        venue = contest.venue
        #venue = Venue.objects.filter(id=venue_id).first()
        return {
            "name": venue.name,
            "image": venue.image_url,
            "address": venue.address,
            "map_file": venue.map_url,
            "description": venue.venue_information,
            "link": venue.website,
            "contest_name": contest.name,
            "judge_link": contest.judge_bio_link,
            "solo_ensemble_link": contest.solo_ensemble_link
            
        }
    
    def build_partner_details(self, contest):
        """
        "partner_details": [
            {
            "image_src": "https://nabba-mobile-app.sfo3.cdn.digitaloceanspaces.com/partner_logos/sparrow-court-logo.png",
            "name": "Sparrow Court Consulting",
            "link": "https://www.sparrowcourt.com",
            "background": "#FFFFFF"
            },
            {
            "image_src": "https://static.wixstatic.com/media/2ecf74_49e7896683be452bafdcc0b3f986f595~mv2.png/v1/fill/w_2100,h_754,fp_0.47_0.34,q_90,enc_auto/2ecf74_49e7896683be452bafdcc0b3f986f595~mv2.png",
            "name": "Patrick Oliverio Studios",
            "link": "https://www.patrickoliverio.com/videos",
            "background": "#FFFFFF"
            },
            {
            "image_src": "https://nabba-mobile-app.sfo3.cdn.digitaloceanspaces.com/partner_logos/brookwright_music_logo.jpg",
            "name": "Brookwright Music",
            "link": "https://www.brookwrightmusic.com/",
            "background": "#241f44"
            }
        ]
        }
        """
        return ""

    def handle(self, *args, **options):
        contest_id = options['contest_id']
        contest_dict = {}
        contest = Contest.objects.get(pk=contest_id)
        print(contest)
        bands = contest.bands.all()
        print(bands)
        # Get list of bands for contest ID provided
        contest_dict["band_list"] = self.build_band_list(bands, contest)
        # Get list of performance slots for contest ID provided
        contest_dict["performance_schedule"] = self.build_performance_schedule(contest)
        # get list of music for contest id provided
        # get venue info for contest id provided
        contest_dict["venue_details"] = self.build_venue_details(contest)
        # get director info for contest ID provided
        # get partners for contest ID provided
        contest_dict["partner_details"] = self.build_partner_details(contest)


        open('contest.json', 'w').write(json.dumps(contest_dict, indent=4, cls=DateTimeEncoder))


        self.stdout.write(self.style.SUCCESS('Contest file generated'))
