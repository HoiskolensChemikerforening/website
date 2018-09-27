import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet

from chemie.customprofile.models import Profile

"""
POTITION_TYPE_CHOICES= (
    ('pHormand/pHorquinde','pHormand/pHorquinde'),
    ('PR-sjaepH','PR-sjaepH'),
    ('Sectreteuse','Sectreteuse'),
    ('Kasserer','Kasserer'),
    ('pHaestsjaepH','pHaestsjaepH'),
    ('IndustrisjaepH','IndustrisjaepH'),
    ('ChemicalsjaepH','ChemicalsjaepH'),
    ('Kjellerstyret','Kjellerstyret'),
    ('Assisterende pHaestsjef','Assisterende pHaestsjef'),
    ('pHaestslave','pHaestslave'),
    ('Redacteur','Redacteur'),
    ('Administrasjonprotogé/sjaepH', 'Administrasjonprotogé/sjaepH'),
    ('Utenrikskomiteen','Utenrikskomiteen'),
    ('Wettrekomiteen','Wettrekomiteen'),
    ('Arrkomiteen','Arrkomiteen'),
    ('Sportskomiteen','Sportskomiteen'),
    ('Arkivar','Arkivar'),
    ('Fadderkomiteen','Fadderkomiteen'),
    ('PTV: (ProgramsTillitsValgt for MTKJ)','PTV: (ProgramsTillitsValgt for MTKJ)'),
    ('Webkomiteen','Webkomiteen')
)"""

"""
---------------READ ME-----------------
- I appen er elections delt inn i to deler, en admin del og en bruker del
- I admindelen vil alt av logikk med stemmetelling og legge til kandidater skjer
- I brukerdelen vil hver bruker kunne stemme på en kandidat når admin gir dem tilgang 
- Valget går ut på at man lager et objekt av Election, det vil si at kun et objekt lages for et medlemsmøte emd valg
- Det legges til unike Position objekter fra lista over som knyttes til election
- Det legges til Candidates objekter knyttet hvert position objekt, disse er hentet fra Django sin User
- For hver position vil det lages nye Candidates-objekter,  
- Dvs: Hvis Joachim stiller til to verv vil User "Joachim" hentes to ganger fra User og danne to Candidates-objekter som er knyttet til hvert sitt position-objekt
- For logikken bak telling av stemmer, se admin_end_voting i views
- Når admin starter valget vil current_position_is_open settes til True og man kan da stemme på en bestemt position
- Når admin slutter valget vil vinnere med flest stemmer lagres i winners og man kan da gå videre til neste valg
---------------------------------------
"""


class Candidate(models.Model):
    user = models.ForeignKey(User, related_name="candidate")
    votes = models.IntegerField(verbose_name="Antall stemmer", blank=True, default=0)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


class Position(models.Model):
    position_name = models.CharField(max_length=100, verbose_name="Navn på verv")
    spots = models.IntegerField(verbose_name="Antall plasser")
    candidates = models.ManyToManyField(Candidate, blank=True, related_name="positions")
    total_votes = models.IntegerField(default=0)
    voting_done = models.BooleanField(default=False)
    winners = models.ManyToManyField(Candidate, blank=True, related_name="winners", default=None)

    def delete_candidates(self, candidates):
        if type(candidates) is Candidate:
            deletable = candidates
            if deletable in self.candidates.all():
                deletable.delete()
                self.save()
                return
        elif type(candidates) is QuerySet:
            deletables = candidates
        elif type(candidates) is list:
            ids = [candidate.id for candidate in candidates]
            deletables = Candidate.objects.filter(pk__in=ids)
        else:
            raise AttributeError
        for candidate in deletables:
            if candidate in self.candidates.all():
                candidate.delete()
            else:
                print('Candidate {} was not related to position {}'.format(candidate, self))
        self.save()

    def __str__(self):
        return self.position_name

    def end_voting_for_position(self):
        if self.candidates.all().count() > 0:
            if self.spots >= self.candidates.all().count():
                winners = self.candidates.all()
                for candidate in self.candidates.all():
                    self.total_votes += candidate.votes
            else:
                winners = []
                all_votes = {}
                for candidate in self.candidates.all():
                    all_votes[candidate.id] = candidate.votes
                    self.total_votes += candidate.votes
                winner_spots = self.spots
                while len(winners) < winner_spots:
                    most_votes = max(all_votes.values())
                    winner_ids = []
                    for candidate_id, votes in all_votes.items():
                        if votes == most_votes:
                            winner_ids.append(candidate_id)
                            # Now set the votes of the last found winner to -1, so he is not found again
                            all_votes[candidate_id] = -1
                    winner_candidates = Candidate.objects.filter(id__in=winner_ids)
                    winners.extend(list(winner_candidates))

            # All winners are now stored in a list. Add this to self.winners
            self.winners.add(*winners)
            self.voting_done = True
            self.save()
        election = Election.objects.latest('id')
        election.current_position_is_open = False
        election.current_position = None
        election.save()


class Election(models.Model):
    is_open = models.BooleanField(verbose_name="Er åpent", default=False) #Generelt for hele valget
    positions = models.ManyToManyField(Position, blank=True, related_name='election')
    current_position = models.ForeignKey(Position, blank=True, null=True, related_name='current_election')
    current_position_is_open = models.BooleanField(verbose_name="Det er åpent for stemming", default=False)  #For delvalget for hver position
    date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.date)

    def add_position(self, positions):
        if type(positions) is Position:
            self.positions.add(positions)
            self.save()
            return
        elif type(positions) is QuerySet:
            self.positions.add(positions)
            self.save()
            return
        elif type(positions) is list:
            self.positions.add(*positions)
            self.save()
        else:
            raise AttributeError

    def delete_position(self, positions):
        if type(positions) is Position:
            position = positions
            position.delete_candidates(candidates=position.candidates.all())
            position.delete()
            self.save()
            return
        elif type(positions) is QuerySet:
            deletables = positions
        elif type(positions) is list:
            ids = [position.id for position in positions]
            deletables = Position.objects.filter(pk__in=ids)
        else:
            raise AttributeError
        for position in deletables:
            if position in self.positions.all():
                position.delete_candidates(candidates=position.candidates.all())
                position.delete()
            else:
                raise ValueError
        self.save()

    def start_current_election(self, current_position):
        # finner posisjonen vi skal votere om
        #current_position = Position.objects.get(id=current_position_id)
        candidates = current_position.candidates.all()
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.voted = False
            profile.save()
        if not self.current_position_is_open:  # forhindrer at vi ikke resetter votes ved refresh page
            self.current_position = current_position
            self.current_position.total_votes = 0
            self.current_position_is_open = True
            # Legge til forhndsstemmene i totale stemmer
            for candidate in candidates:
                self.current_position.total_votes += candidate.votes
            self.current_position.save()
            self.save()

    def end_election(self):
        if self.is_open:
            self.is_open = False
            self.date = datetime.date.today()
            self.save()

    def vote(self, profile, candidates=None, blank=False):
        voted = False
        if not profile.voted:
            if blank:
                self.current_position.total_votes += 1
                self.current_position.save()
                voted = True
                profile.voted = True
                profile.save()
            else:
                if type(candidates) is Candidate:
                    candidate = candidates
                    candidate.votes += 1
                    self.current_position.total_votes += 1
                    candidate.save()
                    self.current_position.save()
                    return True
                elif type(candidates) is QuerySet:
                    cands = candidates
                elif type(candidates) is list:
                    ids = [candidate.id for candidate in candidates]
                    cands = Candidate.objects.filter(pk__in=ids)
                else:
                    raise AttributeError
                if cands.count() is not 0:
                    for candidate in cands:
                        candidate.votes += 1
                        self.current_position.total_votes += 1
                        candidate.save()
                        self.current_position.save()
                    profile.voted = True
                    profile.save()
                    voted = True
        return voted
