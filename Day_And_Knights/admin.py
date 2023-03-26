from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Match, League, Team, Player, Board
from django.contrib.admin.widgets import FilteredSelectMultiple

def reset_matches(modeladmin, request, queryset):
    for league in queryset:
        Match.objects.filter(league=league).delete()

    
reset_matches.short_description = "Reset Matches"

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'home_team', 'away_team', 'league')
    list_filter = ('league',)
    search_fields = ('home_team__name', 'away_team__name')
    date_hierarchy = 'date'

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    actions = [reset_matches]

class TeamAdminForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=FilteredSelectMultiple('Players', is_stacked=False),
        required=False,
    )
    League = forms.ModelMultipleChoiceField(
        queryset=League.objects.all(),
        widget=FilteredSelectMultiple('Leagues', is_stacked=False),
        required=False,
    )

    class Meta:
        model = Team
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['players'].initial = self.instance.players.all()
            self.fields['League'].initial = self.instance.League.all()

class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm
    list_display = ('team_name', 'captain', 'get_leagues')
    search_fields = ('team_name', 'captain__first_name', 'captain__last_name')
    filter_horizontal = ('players', 'League')

    def get_players(self, obj):
        return ", ".join([p.name() for p in obj.players.all()])

    get_players.short_description = 'Players'

    def get_leagues(self, obj):
        return ", ".join([l.name for l in obj.League.all()])

    get_leagues.short_description = 'Leagues'

class PlayerAdminForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=FilteredSelectMultiple("Teams", is_stacked=False),
        required=False,
    )

    def save(self, commit=True):
        player = super(PlayerAdminForm, self).save(commit=False)
        if commit:
            player.save()
        if player.pk:
            player.teams.clear()
            for team in self.cleaned_data['teams']:
                player.teams.add(team)
        return player

    class Meta:
        model = Player
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['teams'].initial = self.instance.teams.all()

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ecf_rating', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    filter_horizontal = ('teams',)
    form = PlayerAdminForm

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'ecf_code')}),
        ('Team', {'fields': ('teams',)}),
    )

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    name.short_description = 'Name'

    def ecf_rating(self, obj):
        return obj.get_ecf_rating()
    ecf_rating.short_description = 'ECF Rating'
    ecf_rating.admin_order_field = 'ecf_code'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('teams')
        return queryset
    

class ResultFilter(admin.SimpleListFilter):
    title = 'Result'
    parameter_name = 'result'

    def lookups(self, request, model_admin):
        return (
            ('1-0', '1-0'),
            ('0-1', '0-1'),
            ('1/2-1/2', '1/2-1/2'),
            ('*', '*'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(result=self.value())
        else:
            return queryset


class BoardAdmin(admin.ModelAdmin):
    list_display = ('match', 'board_number', 'white_player', 'black_player', 'result', 'result_reason')
    list_filter = (ResultFilter,)
    search_fields = ('match__home_team__name', 'match__away_team__name', 'white_player__first_name', 'white_player__last_name', 'black_player__first_name', 'black_player__last_name')
    fieldsets = (
        (None, {
            'fields': ('match', 'board_number', 'white_player', 'black_player', 'result', 'result_reason')
        }),
    )

admin.site.register(Board, BoardAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
