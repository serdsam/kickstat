def calculate_win_loss_ratio(team_name, stadium_name, season_name, competition_name):
    # Query to get scores for matches where the team was playing away
    away_matches = execute_and_return_result(
        'MATCH (a:MatchNode)-[MatchHeldInStadium]->(d:Stadium), (a)-[MatchAwayTeam]->(t:Team), \
         (a)-[MatchHeldInSeason]->(s:Season), (a)-[MatchPartOfCompetition]->(c:Competition) \
         WHERE d.name = "{}" AND t.team_name = "{}" AND s.season_name="{}" AND c.competition_name = "{}" \
         RETURN a.away_score, a.home_score'.format(
            stadium_name, team_name, season_name, competition_name
        )
    )

    # Query to get scores for matches where the team was playing at home
    home_matches = execute_and_return_result(
        'MATCH (a:MatchNode)-[MatchHeldInStadium]->(d:Stadium), (a)-[MatchHomeTeam]->(t:Team), \
         (a)-[MatchHeldInSeason]->(s:Season), (a)-[MatchPartOfCompetition]->(c:Competition) \
         WHERE d.name = "{}" AND t.team_name = "{}" AND s.season_name="{}" AND c.competition_name = "{}" \
         RETURN a.home_score, a.away_score'.format(
            stadium_name, team_name, season_name, competition_name
        )
    )

    win_count = 0
    loss_count = 0

    # Count wins and losses in away matches
    for match in away_matches:
        if match[0] > match[1]:  # Away score > Home score
            win_count += 1
        elif match[0] < match[1]:  # Away score < Home score
            loss_count += 1

    # Count wins and losses in home matches
    for match in home_matches:
        if match[0] > match[1]:  # Home score > Away score
            win_count += 1
        elif match[0] < match[1]:  # Home score < Away score
            loss_count += 1

    # Calculating ratios
    total_games = win_count + loss_count
    if total_games > 0:
        win_ratio = win_count / total_games
        loss_ratio = loss_count / total_games
        return f"Win count: {win_count}, Loss count: {loss_count}, Win Ratio: {win_ratio}, Loss Ratio: {loss_ratio} in {stadium_name}"
    else:
        return f"No games played in {stadium_name}"

    # Test:
    ratio = calculate_win_loss_ratio(
        "Leicester City", "King Power Stadium", "2015/2016", "Premier League"
    )
    print(ratio)
