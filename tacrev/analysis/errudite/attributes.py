from errudite.builts import Attribute

Attribute.create(
    name="gt",
    description="",
    cmd=f"LABEL(groundtruth)"
)

Attribute.create(
    name="groundtruth_label",
    description="",
    cmd="LABEL(groundtruth)"
)


Attribute.create(
    name="arg_types_coarse",
    description="",
    cmd=f"ARG_TYPES_COARSE(LABEL(groundtruth))"
)

Attribute.create(
    name="arg_type_coarse_first",
    description="",
    cmd=f"ARG_TYPES_COARSE_FIRST(LABEL(groundtruth))"
)

Attribute.create(
    name="arg_type_coarse_second",
    description="",
    cmd=f"ARG_TYPES_COARSE_SECOND(LABEL(groundtruth))"
)

Attribute.create(
    name="arg_types_fine",
    description="",
    cmd=f"ARG_TYPES_FINE(LABEL(groundtruth))"
)

Attribute.create(
    name="pos_head",
    description="",
    cmd="TAG(token(text, HEAD_SPAN(text)), get_most_common=True)"
)

Attribute.create(
    name="ent_type_head",
    description="",
    cmd="ENT_TYPE(token(text, HEAD_SPAN(text)), get_most_common=True)"
)

Attribute.create(
    name="ent_type_tail",
    description="",
    cmd="ENT_TYPE(token(text, TAIL_SPAN(text)), get_most_common=True)"
)

Attribute.create(
    name="pos_tail",
    description="",
    cmd="TAG(token(text, TAIL_SPAN(text)), get_most_common=True)"
)

Attribute.create(
    name="sentence_length",
    description="",
    cmd="length(text)"
)

Attribute.create(
    name="argument_distance",
    description="",
    cmd="SPAN_DISTANCE(TAIL_SPAN(text), HEAD_SPAN(text))"
)

Attribute.create(
    name="type_head",
    description="",
    cmd="HEAD_TYPE(text)"
)

Attribute.create(
    name="type_tail",
    description="",
    cmd="TAIL_TYPE(text)"
)

Attribute.create(
    name="count_entity_in_context",
    description="",
    cmd="COUNT_ENTITY_IN_CONTEXT(text)"
)

Attribute.create(
    name="num_distractor_between_arguments",
    description="",
    cmd="NUM_DISTRACTOR_BETWEEN_ARGUMENTS(text)"
)

Attribute.create(
    name="has_inverse_relation",
    description="",
    cmd="HAS_INVERSE_RELATION(LABEL(groundtruth))"
)

Attribute.create(
    name="subj_type",
    description="Argument type of the head/subject argument, based on the TACRED dataset-provided subj_type",
    cmd="HEAD_TYPE(text)"
)

Attribute.create(
    name="coarse_subj_type",
    description="'Coarse' argument type of the head/subject argument, based on the TACRED dataset-provided subj_type and mapped with TACRED_SUBJ_OBJ_TYPES",
    cmd="COARSE_SUBJ_OBJ_TYPE(HEAD_TYPE(text))"
)

Attribute.create(
    name="obj_type",
    description="Argument type of the tail/object argument, based on the TACRED dataset-provided obj_type",
    cmd="TAIL_TYPE(text)"
)

Attribute.create(
    name="coarse_obj_type",
    description="'Coarse' argument type of the tail/object argument, based on the TACRED dataset-provided obj_type and mapped with TACRED_SUBJ_OBJ_TYPES",
    cmd="COARSE_SUBJ_OBJ_TYPE(TAIL_TYPE(text))"
)