"""
serializer.py

Serialize Talk of the Town simulation to JSON
"""
import json
import pathlib
from . import town
from . import life_event
from . import occupation
from . import residence
from . import business
from . import relationship
from .simulation import Simulation

def serialize(sim: Simulation):
    """Serialize Talk of the Town simulation to JSON str"""
    output = {}
    output['year'] = sim.year
    output['true_year'] = sim.true_year
    output['ordinal_date'] = sim.ordinal_date
    output['month'] = sim.month
    output['day'] = sim.day
    output['time_of_day'] = sim.time_of_day
    output['town'] = serialize_town(sim.town)
    output['events'] = serialize_events(sim.events)
    output['birthdays'] = serialize_birthdays(sim.birthdays)
    output['weather'] = sim.weather
    output['last_simulated_day'] = sim.last_simulated_day
    output['n_simulated_timesteps'] = sim.n_simulated_timesteps
    output['stories'] = serialize_stories(sim.story_recognizer)

    return json.dumps(output)

def serialize_to_file(sim: Simulation, filename: pathlib.Path):
    """Serialize Talk of the Town simulation to JSON file"""
    json_str = serialize(sim)
    with open(filename, "w") as f:
        f.write(json_str)

def serialize_stories(story_recognizer):
    """Serialize stories captured by the StoryRecognizer"""
    output = {
        'unrequited_love': [],
        'love_triangles': [],
        'extramarital_romantic_interests': [],
        'asymmetric_friendships': [],
        'misanthropes': [],
        'rivalries': [],
        'sibling_rivalries': [],
        'business_owner_rivalries': []
    }

    for case in story_recognizer.unrequited_love_cases:
        case_data = {
            'lover': case.lover.id,
            'nonreciprocator': case.nonreciprocator.id
        }
        output['unrequited_love'].append(case_data)

    for case in story_recognizer.love_triangles:
        case_data = {
            'first_person': case.first_person.id,
            'second_person': case.second_person.id,
            'third_person': case.third_person.id
        }
        output['love_triangles'].append(case_data)

    for case in story_recognizer.extramarital_romantic_interests:
        case_data = {
            'married_person': case.married_person.id,
            'love_interest': case.love_interest.id
        }
        output['extramarital_romantic_interests'].append(case_data)

    for case in story_recognizer.asymmetric_friendships:
        case_data = {
            'friend': case.friend.id,
            'enemy': case.enemy.id
        }
        output['asymmetric_friendships'].append(case_data)

    for case in story_recognizer.misanthropes:
        case_data = {
            'misanthrope': case.misanthrope.id
        }
        output['misanthropes'].append(case_data)

    for case in story_recognizer.rivalries:
        case_data = {
            'first_person': case.subjects[0].id,
            'second_person': case.subjects[1].id
        }
        output['rivalries'].append(case_data)

    for case in story_recognizer.sibling_rivalries:
        case_data = {
            'first_person': case.subjects[0].id,
            'second_person': case.subjects[1].id
        }
        output['sibling_rivalries'].append(case_data)

    for case in story_recognizer.business_owner_rivalries:
        case_data = {
            'subjects': [p.id for p in case.subjects],
            'companies': [c.id for c in case.companies],
            'industry': case.industry
        }
        output['business_owner_rivalries'].append(case_data)

    return output

def serialize_town(town):
    """Serialize Talk of the Town town"""
    output = {
        "founded": town.founded,
        "places": {},
        "people": {},
        "streets": {},
        "lots": {},
        "tracts": {},
        "parcels": {},
        "dwelling_places": [],
        "blocks": {},
        "apartment_complexes": [],
        "other_businesses": [],
        "houses": [],
        "settlers": [],
        "residents": [],
        "departed": [],
        "deceased": [],
        "companies": [],
        "former_companies": [],
        "paths": {},
        "downtown": town.downtown.id if town.downtown else -1,
        "cemetery": town.cemetery.id if town.cemetery else -1,
        "city_hall": town.city_hall.id if town.city_hall else -1,
        "fire_station": town.fire_station.id if town.fire_station else -1,
        "hospital": town.hospital.id if town.hospital else -1,
        "police_station": town.police_station.id if town.police_station else -1,
        "school": town.school.id if town.school else -1,
        "university": town.university.id if town.university else -1
    }

    for c in town.apartment_complexes:
        output["places"][str(c.id)] = serialize_business(c)
        output["apartment_complexes"].append(c.id)

    for b in town.other_businesses:
        output["places"][str(b.id)] = serialize_business(b)
        output["other_businesses"].append(b.id)

    for h in town.houses:
        output["places"][str(h.id)] = serialize_dwelling(h)
        output["houses"].append(h.id)

    for s in town.settlers:
        output["people"][str(s.id)] = serialize_person(s)
        output["settlers"].append(s.id)

    for r in town.residents:
        output["people"][str(r.id)] = serialize_person(r)
        output["residents"].append(r.id)

    for d in town.departed:
        output["people"][str(d.id)] = serialize_person(d)
        output["departed"].append(d.id)

    for d in town.deceased:
        output["people"][str(d.id)] = serialize_person(d)
        output["deceased"].append(d.id)

    for c in town.companies:
        output["places"][str(c.id)] = serialize_business(c)
        output["companies"].append(c.id)

    for c in town.former_companies:
        output["places"][str(c.id)] = serialize_business(c)
        output["former_companies"].append(c.id)

    for l in town.lots:
        output["lots"][str(l.id)] = serialize_lot(l)

    for t in town.tracts:
        output["tracts"][str(t.id)] = serialize_lot(t)

    for d in town.dwelling_places:
        output["places"][str(d.id)] = serialize_dwelling(d)
        output["dwelling_places"].append(d.id)

    for s in town.streets:
        output["streets"][str(s.id)] = serialize_street(s)

    for p in town.parcels:
        output["parcels"][str(p.id)] = serialize_parcel(p)

    for b in town.blocks:
        output["blocks"][str(id(b))] = serialize_block(b)

    for p in town.paths:
        path_key = "{}_{}".format(p[0].id, p[1].id)
        output["paths"][path_key] = town.paths[p]

    return output

def serialize_dwelling(d):
    """Serialize DwellingPlace object"""
    output = {
        "id": d.id,
        "type": d.type,
        "town": d.town.name,
        "lot": d.lot.id if d.lot else -1,
        "house": d.house,
        "apartment": d.apartment,
        "address": d.address,
        "house_number": d.house_number,
        "block": id(d.block),
        "residents": [r.id for r in d.residents],
        "former_residents": [r.id for r in d.former_residents],
        "transactions": [t.event_id for t in d.transactions],
        "move_ins": [e.event_id for e in d.move_ins],
        "move_outs": [e.event_id for e in d.move_outs],
        "owners": [o.id for o in d.owners],
        "former_owners": [o.id for o in d.former_owners],
        "people_here_now": [p.id for p in d.people_here_now],
        "demolition": d.demolition.event_id if d.demolition else -1
    }

    if type(d) is residence.Apartment:
        output["complex"] = d.complex.id if d.complex else -1
        output["unit_number"] = d.unit_number

    if type(d) is residence.House:
        output["construction"] = d.construction.event_id if d.construction else -1

    return output

def serialize_street(s):
    """Serialize Street object"""
    output = {
        "id": s.id,
        "town": s.town.name,
        "number": s.number,
        "direction": s.direction,
        "name": s.name,
        "starting_parcel": s.starting_parcel,
        "ending_parcel": s.ending_parcel,
        "blocks": [id(b) for b in s.blocks]
    }
    return output

def serialize_block(b):
    """Serialize block object"""
    output = {
        "id": id(b),
        "number": b.number,
        "lots": [l.id for l in b.lots],
        "type": b.type,
    }
    return output

def serialize_parcel(p):
    """Serialize Parcel object"""
    output = {
        "id": p.id,
        "street": p.street.id,
        "number": p.number,
        "lots": [l.id for l in p.lots],
        "neighbors": [n.id for n in p.neighbors],
        "coords": [p.coords[0], p.coords[1]]
    }
    return output

def serialize_lot(l):
    """Serialize Lot object"""
    output = {
        "id": l.id,
        "lot": l.lot,
        "tract": l.tract,
        "town": l.town.name,
        "streets": [s.id for s in l.streets],
        "parcels": [p.id for p in l.parcels],
        "block": id(l.block) if l.block else -1,
        "sides_of_street": l.sides_of_street,
        "house_numbers": l.house_numbers,
        "building": l.building.id if l.building else -1,
        "positions_in_city_blocks": l.positions_in_city_blocks,
        "neighboring_lots": [n.id for n in l.neighboring_lots],
        "coordinates": [l.coordinates[0], l.coordinates[1]],
        "house_number": l.house_number if l.house_number else -1,
        "address": l.address if l.address else "",
        "street_address_is_on": l.street_address_is_on.id if l.street_address_is_on else -1,
        "parcel_address_is_on": l.parcel_address_is_on.id if l.parcel_address_is_on else -1,
        "index_of_street_address_will_be_on": l.index_of_street_address_will_be_on if l.index_of_street_address_will_be_on else -1,
        "former_buildings": [b.id for b in l.former_buildings]
    }

    if (type(l) == town.Tract):
        output["size"] = l.size

    return output

def serialize_person(p):
    """Serialize Person object"""
    output = {
            "id": p.id,
            "type": p.type,
            "birth": p.birth.event_id if p.birth else -1,
            "town": p.town.name if p.town else "",
            "biological_mother": p.biological_mother.id if p.biological_mother else -1,
            "mother": p.mother.id if p.mother else -1,
            "biological_father": p.biological_father.id if p.biological_father else -1,
            "father": p.father.id if p.father else -1,
            "parents": [x.id for x in p.parents],
            "birth_year": p.birth_year,
            "age": p.age,
            "adult": p.adult,
            "in_work_force": p.in_the_workforce,
            "male": p.male,
            "female": p.female,
            "tag": p.tag,
            "alive": p.alive,
            "death_year": p.death_year if p.death_year else -1,
            "gravestone": -1,
            "home": p.home.id if p.home else -1,
            "infertile": p.infertile,
            "attracted_to_men": p.attracted_to_men,
            "attracted_to_women": p.attracted_to_women,
            "face": serialize_face(p.face),
            "personality": serialize_personality(p.personality),
            "mind": serialize_mind(p.mind),
            "routine": serialize_routine(p.routine),
            "whereabouts": serialize_whereabouts(p.whereabouts),
            "first_name": p.first_name if p.first_name else "",
            "middle_name": p.middle_name if p.middle_name else "",
            "last_name": p.last_name if p.last_name else "",
            "suffix": p.suffix if p.suffix else "",
            "maiden_name": p.maiden_name if p.maiden_name else "",
            "named_for": [ x.id for x in p.named_for if x ] if p.named_for else [],
            "ancestors": [ x.id for x in p.ancestors ],
            "descendants": [ x.id for x in p.descendants ],
            "immediate_family": [ x.id for x in p.immediate_family ],
            "extended_family": [ x.id for x in p.extended_family ],
            "greatgrandparents": [ x.id for x in p.greatgrandparents ],
            "grandparents": [ x.id for x in p.grandparents ],
            "aunts": [ x.id for x in p.aunts ],
            "uncles": [ x.id for x in p.uncles ],
            "siblings": [ x.id for x in p.siblings ],
            "full_siblings": [ x.id for x in p.full_siblings ],
            "half_siblings": [ x.id for x in p.half_siblings ],
            "brothers": [ x.id for x in p.brothers ],
            "full_brothers": [ x.id for x in p.full_brothers ],
            "half_brothers": [ x.id for x in p.half_brothers ],
            "sisters": [ x.id for x in p.sisters ],
            "full_sisters": [ x.id for x in p.full_sisters ],
            "half_sisters": [ x.id for x in p.half_sisters ],
            "cousins": [ x.id for x in p.cousins ],
            "kids": [ x.id for x in p.kids ],
            "sons": [ x.id for x in p.sons ],
            "daughters": [ x.id for x in p.daughters ],
            "nephews": [ x.id for x in p.nephews ],
            "nieces": [ x.id for x in p.nieces ],
            "grandchildren": [ x.id for x in p.grandchildren ],
            "grandsons": [ x.id for x in p.grandsons ],
            "granddaughters": [ x.id for x in p.granddaughters ],
            "greatgrandchildren": [ x.id for x in p.greatgrandchildren ],
            "greatgrandsons": [ x.id for x in p.greatgrandsons ],
            "greatgranddaughters": [ x.id for x in p.greatgranddaughters ],
            "bio_parents": [ x.id for x in p.bio_parents ],
            "bio_grandparents": [ x.id for x in p.bio_grandparents ],
            "bio_siblings": [ x.id for x in p.bio_siblings ],
            "bio_full_siblings": [ x.id for x in p.bio_full_siblings ],
            "bio_half_siblings": [ x.id for x in p.bio_half_siblings ],
            "bio_brothers": [ x.id for x in p.bio_brothers ],
            "bio_full_brothers": [ x.id for x in p.bio_full_brothers ],
            "bio_half_brothers": [ x.id for x in p.bio_half_brothers ],
            "bio_sisters": [ x.id for x in p.bio_sisters ],
            "bio_full_sisters": [ x.id for x in p.bio_full_sisters ],
            "bio_half_sisters": [ x.id for x in p.bio_half_sisters ],
            "bio_immediate_family": [ x.id for x in p.bio_immediate_family ],
            "bio_greatgrandparents": [ x.id for x in p.bio_greatgrandparents ],
            "bio_uncles": [ x.id for x in p.bio_uncles ],
            "bio_aunts": [ x.id for x in p.bio_aunts ],
            "bio_cousins": [ x.id for x in p.bio_cousins ],
            "bio_nephews": [ x.id for x in p.bio_nephews ],
            "bio_nieces": [ x.id for x in p.bio_nieces ],
            "bio_ancestors": [ x.id for x in p.bio_ancestors ],
            "bio_extended_family": [ x.id for x in p.bio_extended_family ],
            "spouse": p.spouse.id if p.spouse else -1,
            "widowed": p.widowed,
            "relationships": [], # TODO create determine if relationship objects are shared
            "sexual_partners": [x.id for x in p.sexual_partners],
            "acquaintances": [x.id for x in p.acquaintances],
            "friends": [x.id for x in p.friends],
            "enemies": [x.id for x in p.enemies],
            "neighbors": [x.id for x in p.neighbors],
            "former_neighbors": [x.id for x in p.former_neighbors],
            "coworkers": [x.id for x in p.coworkers],
            "former_coworkers": [x.id for x in p.former_coworkers],
            "best_friend": p.best_friend.id if p.best_friend else -1,
            "worst_enemy": p.worst_enemy.id if p.worst_enemy else -1,
            "love_interest": p.love_interest.id if p.love_interest else -1,
            "significant_other": p.significant_other.id if p.significant_other else -1,
            "charge_of_best_friend": p.charge_of_best_friend,
            "charge_of_worst_enemy": p.charge_of_worst_enemy,
            "spark_of_love_interest": p.spark_of_love_interest,
            "talked_to_this_year": [x.id for x in p.talked_to_this_year],
            "befriended_this_year": [x.id for x in p.befriended_this_year],
            "salience_of_other_people": {x.id: p.salience_of_other_people[x] for x in p.salience_of_other_people},
            "pregnant": p.pregnant,
            "impregnated_by": p.impregnated_by.id if p.impregnated_by else -1,
            "conception_year": p.conception_year if p.conception_year else -1,
            "due_date": p.due_date if p.due_date else -1,
            "adoption": p.adoption.event_id if p.adoption else -1,
            "marriage": p.marriage.event_id if p.marriage else -1,
            "marriages": [x.event_id for x in p.marriages],
            "divorces": [x.event_id for x in p.divorces],
            "adoptions": [x.event_id for x in p.adoptions],
            "moves": [x.event_id for x in p.moves],
            "lay_offs": [x.event_id for x in p.lay_offs],
            "name_changes": [x.event_id for x in p.name_changes],
            "building_commissions": [x.event_id for x in p.building_commissions],
            "home_purchases": [x.event_id for x in p.home_purchases],
            "retirement": p.retirement.event_id if p.retirement else -1,
            "departure": p.departure.event_id if p.departure else -1,
            "death": p.death.event_id if p.death else -1,
            "money": p.money,
            "occupation": serialize_occupation(p.occupation) if p.occupation else {},
            "occuptions": [serialize_occupation(o) for o in p.occupations],
            "former_contractors": [o.person.id for o in p.former_contractors],
            "retired": p.retired,
            "college_graduate": p.college_graduate,
            "grieving": p.grieving,
            "location": p.location.id if p.location else -1,
            "wedding_ring_on_finger": p.wedding_ring_on_finger if p.wedding_ring_on_finger else False
        }

    return output

def serialize_face(f):
    """Serialize Face object"""

    def serialize_feature(f):
        return  {
            "value": f,
            "variant_id": f.variant_id,
            "inherited_from": f.inherited_from.id if f.inherited_from else -1,
            "exact_variant_inherited": f.exact_variant_inherited
        }

    def serialize_skin(s):
        return {
            "color": serialize_feature(s.color)
        }

    def serialize_head(h):
        return {
            "size": serialize_feature(h.size),
            "shape": serialize_feature(h.shape)
        }

    def serialize_hair(h):
        return {
            "length": serialize_feature(h.length),
            "color": serialize_feature(h.color)
        }

    def serialize_eyebrows(e):
        return {
            "size": serialize_feature(e.size),
            "color": serialize_feature(e.color)
        }

    def serialize_eyes(e):
        return {
            "size": serialize_feature(e.size),
            "shape": serialize_feature(e.shape),
            "color": serialize_feature(e.color),
            "horizontal_settedness": serialize_feature(e.horizontal_settedness),
            "vertical_settedness": serialize_feature(e.vertical_settedness)
        }

    def serialize_ears(e):
        return {
            "size": serialize_feature(e.size),
            "angle": serialize_feature(e.angle)
        }

    def serialize_nose(n):
        return {
            "size": serialize_feature(n.size),
            "shape": serialize_feature(n.shape)
        }

    def serialize_mouth(m):
        return {
            "size": serialize_feature(m.size)
        }

    def serialize_facial_hair(fh):
        return {
            "style": serialize_feature(fh.style)
        }

    def serialize_distinctive_features(df):
        return {
            "freckles": serialize_feature(df.freckles),
            "birthmark": serialize_feature(df.birthmark),
            "scar": serialize_feature(df.scar),
            "tattoo": serialize_feature(df.tattoo),
            "glasses": serialize_feature(df.glasses),
            "sunglasses": serialize_feature(df.sunglasses)
        }


    output = {
        "person": f.person.id,
        "skin": serialize_skin(f.skin),
        "head": serialize_head(f.head),
        "hair": serialize_hair(f.hair),
        "eyebrows": serialize_eyebrows(f.eyebrows),
        "eyes": serialize_eyes(f.eyes),
        "ears": serialize_ears(f.ears),
        "nose": serialize_nose(f.nose),
        "mouth": serialize_mouth(f.mouth),
        "facial_hair": serialize_facial_hair(f.facial_hair),
        "distinctive_features": serialize_distinctive_features(f.distinctive_features)
    }

    return output

def serialize_relationship(r):
    """Serialize Relationship object"""
    output = {
        "type": r.type,
        "owner": r.owner.id if r.owner else -1,
        "subject": r.subject.id if r.subject else -1,
        "preceded_by": id(r.preceded_by) if r.preceded_by else -1,
        "succeeded_by": id(r.succeeded_by) if r.succeeded_by else -1,
        "where_they_met": r.where_they_met.id if r.where_they_met else -1,
        "when_they_met": r.when_they_met,
        "first_met_str": r.first_met_str,
        "where_they_last_met": r.where_they_last_met.id if r.where_they_last_met else -1,
        "when_they_last_met": r.when_they_last_met,
        "last_met_str_base": r.last_met_str_base,
        "total_interactions": r.total_interactions,
        "compatibility": r.compatibility,
        "raw_charge_increment": r.raw_charge_increment,
        "raw_charge": r.raw_charge,
        "raw_spark_increment": r.raw_spark_increment,
        "raw_spark": r.raw_spark,
        "charge": r.charge,
        "spark": r.spark,
        "age_difference_effect_on_charge_increment": r.age_difference_effect_on_charge_increment if r.age_difference_effect_on_charge_increment else 0,
        "age_difference_effect_on_spark_increment": r.age_difference_effect_on_spark_increment if r.age_difference_effect_on_spark_increment else 0,
        "job_level_difference_effect_on_charge_increment": r.job_level_difference_effect_on_charge_increment if r.job_level_difference_effect_on_charge_increment else 0,
        "job_level_difference_effect_on_spark_increment": r.job_level_difference_effect_on_spark_increment if r.job_level_difference_effect_on_spark_increment else 0,
        "interacted_this_timestep": r.interacted_this_timestep,
        "conversations": []
    }

    return output

def serialize_personality(p):
    """Serialize Personality object"""
    output = {
        "person": p.person.id,
        "openness_to_experience": p.openness_to_experience,
        "conscientiousness": p.conscientiousness,
        "extroversion": p.extroversion,
        "agreeableness": p.agreeableness,
        "neuroticism": p.neuroticism,
        "interest_in_history": p.interest_in_history,
        "high_o": p.high_o,
        "low_o": p.low_o,
        "high_c": p.high_c,
        "low_c": p.low_c,
        "high_e": p.high_e,
        "low_e": p.low_e,
        "high_a": p.high_a,
        "low_a": p.low_a,
        "high_n": p.high_n,
        "low_n": p.low_n
    }
    return output

def serialize_mind(m):
    """Serialize Mind object"""

    def serialize_feature(f):
        """Searialize Feature Object"""
        return {
            "inherited_from": f.inherited_from.id if f.inherited_from else -1,
            "value": f
        }

    output = {
        "person": m.person.id,
        "memory": serialize_feature(m.memory)
    }
    return output

def serialize_routine(r):
    """Serialize Routine object"""
    return {
        "person": r.person.id,
        "working": r.working,
        "occasion": r.occasion if r.occasion else ""
    }

def serialize_birthdays(birthdays: dict):
    output = {}
    for day in birthdays:
        shared_birthdays = birthdays[day]
        output['{}_{}'.format(day[0], day[1])] = [x.id for x in shared_birthdays]
    return output

def serialize_whereabouts(obj):
    """Serialize Whereabouts object"""

    def serialize_single_whereabout(wb):
        """Serialize a single whereabout.Whereabout object"""
        output = {
            "person": wb.person.id,
            "location": wb.location.id,
            "occasion": wb.occasion,
            "date": wb.date,
            "ordinal_date": wb.ordinal_date,
            "time_of_day": wb.time_of_day
        }

        return output

    def serialize_dates(dates: dict):
        output = {}

        for key in dates:
            date_key = "{}_{}".format(key[0], key[1])
            output[date_key] = serialize_single_whereabout(dates[key])

        return output

    output = {
        "person": obj.person.id,
        "date": serialize_dates(obj.date)
    }

    return output

def serialize_events(events: list):
    output = {}

    for event in events:
        entry = {
            "event_id": event.event_id,
            "type": event.__class__.__name__,
            "year": event.date.year,
            "month": event.date.month,
            "day": event.date.day,
            "ordinal_date": event.date.toordinal()
        }

        if type(event) is life_event.Adoption:
            entry["town"] = event.town.name if event.town else ""
            entry["subject"] = event.subject.id
            entry["adoptive_parents"] = [x.id for x in event.adoptive_parents]

        if type(event) is life_event.Birth:
            entry["town"] = event.town.name if event.town else ""
            entry["biological_mother"] = event.biological_mother.id
            entry["mother"] = event.biological_mother.id
            entry["biological_father"] = event.biological_father.id
            entry["father"] = event.father.id
            entry["subject"] = event.subject.id
            entry["doctor"] = event.doctor.person.id if event.doctor else -1
            entry["hospital"] = event.hospital.id if event.hospital else -1
            entry["nurses"] = [x.person.id for x in event.nurses]

        if type(event) is life_event.BusinessConstruction:
            entry["subject"] = event.subject.id
            entry["architect"] = event.architect.person.id if event.architect else -1
            entry["business"] = event.business.id
            entry["construction_firm"] = event.construction_firm.id if event.construction_firm else -1
            entry["builders"] = [x.id for x in event.builders]

        if type(event) is life_event.BusinessClosure:
            entry["town"] = event.town.name if event.town else ""
            entry["business"] = event.business.id
            entry["reason"] = event.reason.event_number if event.reason else -1

        if type(event) is life_event.Death:
            entry["town"] = event.town.name if event.town else ""
            entry["subject"] = event.subject.id
            entry["widow"] = event.widow.id if event.widow else -1
            entry["cause"] = event.cause
            entry["mortician"] = event.mortician.person.id if event.mortician else -1
            entry["cemetery"] = event.cemetery.id if event.cemetery else -1
            entry["next_of_kin"] = event.next_of_kin.id if event.next_of_kin else -1
            entry["cemetery_plot"] = event.cemetery_plot if event.cemetery_plot else -1

        if type(event) is life_event.Demolition:
            entry["town"] = event.town.name
            entry["building"] = event.building.id
            entry["reason"] = event.reason.event_id

        if type(event) is life_event.Departure:
            entry["subject"] = event.subject.id

        if type(event) is life_event.Divorce:
            entry["town"] = event.town.name
            entry["subjects"] = [x.id for x in event.subjects]
            entry["lawyer"] = event.lawyer.person.id if event.lawyer else -1
            entry["marriage"] = event.marriage.event_id
            entry["law_firm"] = event.law_firm.id if event.law_firm else -1

        if type(event) is life_event.Hiring:
            entry["subject"] = event.subject.id
            entry["company"] = event.company.id
            entry["occupation"] = id(event.occupation)
            entry["old_occupation"] = id(event.old_occupation)

        if type(event) is life_event.HomePurchase:
            entry["town"] = event.town.name
            entry["subjects"] = [x.id for x in event.subjects]
            entry["home"] = event.home.id
            entry["realtor"] = event.realtor.person.id if event.realtor else -1
            entry["realty_firm"] = event.realty_firm.id if event.realty_firm else -1

        if type(event) is life_event.HouseConstruction:
            entry["subjects"] = [x.id for x in event.subjects]
            entry["architect"] = event.architect.person.id if event.architect else -1
            entry["house"] = event.house.id
            entry["construction_firm"] = event.construction_firm.id if event.construction_firm else -1
            entry["builders"] = [x.person.id for x in event.builders]

        if type(event) is life_event.LayOff:
            entry["subject"] = event.subject.id
            entry["company"] = event.company.id
            entry["reason"] = event.reason.event_id if event.reason else -1
            entry["occupation"] = serialize_occupation(event.occupation) if event.occupation else {}

        if type(event) is life_event.Marriage:
            entry["town"] = event.town.name if event.town else ""
            entry["subjects"] = [x.id for x in event.subjects]
            entry["names_at_time_of_marriage"] = [x for x in event.names_at_time_of_marriage]
            entry["name_changes"] = [x.event_id for x in event.name_changes]
            entry["terminus"] = event.terminus.event_id if event.terminus else -1
            entry["money"] = event.money if event.money else 0
            entry["children_produced"] = [x.id for x in event.children_produced]

        if type(event) is life_event.Move:
            entry["subjects"] = [x.id for x in event.subjects]
            entry["old_home"] = event.old_home.id if event.old_home else -1
            entry["new_home"] = event.new_home.id if event.new_home else -1
            entry["reason"] = event.reason.event_id if event.reason else -1

        if type(event) is life_event.NameChange:
            entry["town"] = event.town.name if event.town else ""
            entry["subject"] = event.subject.id
            entry["old_last_name"] = event.old_last_name
            entry["new_last_name"] = event.new_last_name
            entry["old_name"] = event.old_name
            entry["lawyer"] = event.lawyer.person.id if event.lawyer else -1
            entry["new_name"] = event.new_name
            entry["reason"] = event.reason.event_id if event.reason else -1
            entry["law_firm"] = event.law_firm.id if event.law_firm else -1

        if type(event) is life_event.Retirement:
            entry["subject"] = event.subject.id
            entry["occupation"] = serialize_occupation(event.occupation)
            entry["company"] = event.company.id

        output[event.event_id] = entry

    return output

def serialize_occupation(job):
    output = {
        "type": job.__class__.__name__,
        "person": job.person.id,
        "company": job.company.id,
        "shift": job.shift,
        "start_date": job.start_date,
        "hiring": job.hiring.event_id if job.hiring else -1,
        "end_date": job.end_date,
        "terminus": job.terminus.event_id if job.terminus else -1,
        "preceded_by": job.preceded_by.person.id if job.preceded_by else -1,
        "succeeded_by": job.succeeded_by.person.id if job.succeeded_by else -1,
        "supplemental": job.supplemental,
        "hired_as_favor": job.hired_as_favor,
        "vocation": job.vocation,
        "level": job.level
    }

    if type(job) is occupation.Architect:
        output["building_constructions"] = [e.event_id for e in job.building_constructions]
        output["house_constructions"] = [e.event_id for e in job.house_constructions]

    if type(job) is occupation.Doctor:
        output["baby_deliveries"] = [e.event_id for e in job.baby_deliveries]

    if type(job) is occupation.Lawyer:
        output["filed_divorces"] = [e.event_id for e in job.filed_divorces]
        output["filed_name_changes"] = [e.event_id for e in job.filed_name_changes]

    if type(job) is occupation.Mortician:
        output["body_interments"] = [e.event_id for e in job.body_interments]

    if type(job) is occupation.Realtor:
        output["home_sales"] = [e.event_id for e in job.home_sales]



    return output

def serialize_business(b):
    """Serialize Business object"""
    output = {
        "id": b.id,
        "type": b.type,
        "demise": b.demise,
        "services": list(b.services),
        "town": b.town.name,
        "founded": b.founded,
        "lot": b.lot.id,
        "employees": [x.person.id for x in b.employees],
        "former_employees": [x.person.id for x in b.former_employees],
        "former_owners": [x.person.id for x in b.former_owners],
        "supplemental_vacancies": {shift: [o.__name__ for o in b.supplemental_vacancies[shift]] for shift in b.supplemental_vacancies},
        "construction": b.construction.event_id if b.construction else -1,
        "address": b.address,
        "house_number": b.house_number,
        "street_address_is_on": b.street_address_is_on.id if b.street_address_is_on else -1,
        "block": id(b.block) if b.block else -1,
        "name": b.name if b.name else "",
        "people_here_now": [x.id for x in b.people_here_now],
        "demolition": b.demolition.event_id if b.demolition else -1,
        "out_of_business": b.out_of_business,
        "closure": b.closure.event_id if b.closure else -1,
        "closed": b.closed if b.closed else -1
    }

    if type(b) is business.ApartmentComplex:
        output["units"] = [x.id for x in b.units]

    if type(b) is business.Cemetery:
        output["plots"] = {x: b.plots[x].id for x in b.plots}


    return output
