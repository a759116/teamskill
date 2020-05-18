"""This code demonstrates creation of nodes and relationship between those: create_sample_data. And then it
demonstrates some sample queries, using both techniques provided by neomodel and cypher query: Refer  sample_queries
"""

from typing import Any, Union

from model import Skill, TeamMember, ProficiencyRel
from neomodel import db, Q


def create_sample_data():
    # create skills
    python: Union[Skill, Any] = Skill(name="Python").save()
    fim_process = Skill(name="FIM Process").save()
    neo4j = Skill(name="neo4j").save()
    data_engineering = Skill(name="Data Engineering").save()
    data_visualization = Skill(name="Data Visualization").save()

    # create team members and connect to skill
    tom = TeamMember(first_name="Tom", last_name="Holiday").save()
    tom.skill.connect(python, {'year': 2019, 'score': 4.0})
    tom.skill.connect(fim_process, {'year': 2019, 'score': 5.0})
    tom.skill.connect(python, {'year': 2020, 'score': 5.0})
    tom.skill.connect(fim_process, {'year': 2020, 'score': 5.0})
    tran = TeamMember(first_name="Tran", last_name="Charismatic").save()
    tran.skill.connect(python, {'year': 2019, 'score': 3.0})
    ron = TeamMember(first_name="Ron", last_name="Paradise").save()
    ron.skill.connect(neo4j, {'year': 2019, 'score': 2.0})
    ron.skill.connect(python, {'year': 2019, 'score': 3.0})
    ron.skill.connect(data_engineering, {'year': 2019, 'score': 5.0})
    dev = TeamMember(first_name="Dev", last_name="Global").save()
    dev.skill.connect(data_engineering, {'year': 2019, 'score': 4.0})
    dev.skill.connect(data_visualization, {'year': 2019, 'score': 3.0})
    aqua = TeamMember(first_name="Aqua", last_name="Gloss").save()
    aqua.skill.connect(data_visualization, {'year': 2019, 'score': 2.0})
    aqua.skill.connect(python, {'year': 2019, 'score': 2.0})
    prem = TeamMember(first_name="Prem", last_name="Chopra").save()
    prem.skill.connect(fim_process, {'year': 2019, 'score': 3.0})

# this demonstrates use of cycpher query and interpretation of result returned from the query
def sample_describe_graph():
    rows, cols = db.cypher_query("MATCH (t:TeamMember)-[p:PROFICIENCY_FOR]-(s:Skill)"
                                 " RETURN t, p, s")
    for r in rows:  # cols {0: TeamMember, 1: Proficiency, 2: Skill}
        team_member = TeamMember.inflate(r[0])
        proficiency = ProficiencyRel.inflate(r[1])
        skill = Skill.inflate(r[2])
        print("Team member {} is proficient in skill {} with a score {} in year {}  \n"
              .format(team_member.name, skill.name, proficiency.score, proficiency.year))


def sample_queries():
    # use objects to query for information
    print("Find Skill Python: {} ".format(Skill.nodes.get_or_none(name="Python")))
    print("Find Skill Java that doesn't exist: {} ".format(Skill.nodes.get_or_none(name="Java")))
    print("Find all team members name that starts with T: \n")
    team_members = TeamMember.nodes.filter(Q(first_name__startswith='T'))
    for n in team_members:
        print("\tTeam member: {}\n".format(n))

    print("Team members name that starts with T have proficiencies more than 3 in: \n")
    excellencies = team_members.skill.match(score__gt=4.0)
    for ex in excellencies:
        print("\t Skills: {} \n".format(ex))

    # use cypher queries
    print("Current graph description: ")
    sample_describe_graph()

    print("Print the skills in which team member first name starting with T has score more than 3 in any year")
    rows, cols = db.cypher_query("MATCH(t: TeamMember)-[p: PROFICIENCY_FOR]-(s:Skill) "
                                 "WHERE t.first_name STARTS WITH 'T' AND p.score > 3.0 "
                                 "RETURN DISTINCT (s)")
    for r in rows:
        skill = Skill.inflate(r[0])  # cols: {0: Skill}
        print("Skill name {} ".format(skill.name))

    print("For each of the available skills, find out the list of team members who has proficiency in it\n")
    skills = Skill.nodes.all()
    for skill in skills:
        rows, cols = db.cypher_query("MATCH (s:Skill)-[p:PROFICIENCY_FOR]-(t:TeamMember) "
                                     "WHERE s.name = $name RETURN DISTINCT (t)", params={"name": skill.name})
        print("\nSkill name: {} ".format(skill.name))
        for r in rows:
            team_member = TeamMember.inflate(r[0])  # cols: {0: TeamMember}
            print("Team member name {} ".format(team_member.name))


if __name__ == '__main__':
    # delete existing data prior to loading
    results, meta = db.cypher_query("MATCH (s:Skill) DETACH DELETE (s)")
    results, meta = db.cypher_query("MATCH (t:TeamMember) DETACH DELETE (t)")
    # load sample data
    create_sample_data()
    # sample queries
    sample_queries()
