from typing import Tuple

from tacrev.definitions import RELATION_DEFS, TACRED_SUBJ_OBJ_TYPES, INVERSE_RELATIONS
from errudite.targets import Instance, Target
from errudite.build_blocks import PrimFunc

from itertools import groupby

@PrimFunc.register()
def ARG_TYPES_COARSE(label: str) -> str:
    """
    The coarse grained argument types of a relation label, e.g. per:loc
    """
    output = None
    try:
        relation_def = RELATION_DEFS[label]
        output = f"{relation_def[0][0]}:{relation_def[1][0]}"
    except Exception as e:
        ex = Exception(f"Unknown exception from [ ARG_TYPES_COARSE ]: {e}")
        raise(ex)
    else:
        return output


@PrimFunc.register()
def ARG_TYPES_FINE(label: str) -> str:
    """
    The fine grained argument types of a relation label, e.g. per:country
    """
    output = None
    try:
        relation_def = RELATION_DEFS[label]
        output = f"{relation_def[0][0]}:{relation_def[1][0]}-{relation_def[1][1]}"
    except Exception as e:
        ex = Exception(f"Unknown exception from [ ARG_TYPES_FINE ]: {e}")
        raise(ex)
    else:
        return output
    
    
@PrimFunc.register()
def LABEL_CONTAINS(label: str, substr) -> str:
    """
    The fine grained argument types of a relation label, e.g. per:country
    """
    output = None
    try:
        output = substr in label
    except Exception as e:
        ex = Exception(f"Unknown exception from [ LABEL_CONTAINS ]: {e}")
        raise(ex)
    else:
        return output
    
    
@PrimFunc.register()
def HEAD_SPAN(target: Target) -> str:
    """
    The head entity's span
    """
    output = None
    try:
        output = target.head
    except Exception as e:
        ex = Exception(f"Unknown exception from [ HEAD_SPAN ]: {e}")
        raise(ex)
    else:
        return output
    
    
@PrimFunc.register()
def TAIL_SPAN(target: Target) -> str:
    """
    The tail entity's span
    """
    output = None
    try:
        output = target.tail
    except Exception as e:
        ex = Exception(f"Unknown exception from [ TAIL_SPAN ]: {e}")
        raise(ex)
    else:
        return output
    
    
@PrimFunc.register()
def SPAN_DISTANCE(span1: Tuple[int, int], span2: Tuple[int, int], absolute=False) -> str:
    """
    The distance between two spans
    """
    output = None
    try:
        output = span2[0] - span1[0]
    except Exception as e:
        ex = Exception(f"Unknown exception from [ SPAN_DISTANCE ]: {e}")
        raise(ex)
    else:
        return output


@PrimFunc.register()
def HEAD_TYPE(target: Target) -> str:
    """
    The head entity's type
    """
    output = None
    try:
        output = target.head_type
    except Exception as e:
        ex = Exception(f"Unknown exception from [ HEAD_TYPE ]: {e}")
        raise(ex)
    else:
        return output


@PrimFunc.register()
def TAIL_TYPE(target: Target) -> str:
    """
    The tail entity's type
    """
    output = None
    try:
        output = target.tail_type
    except Exception as e:
        ex = Exception(f"Unknown exception from [ TAIL_TYPE ]: {e}")
        raise(ex)
    else:
        return output

@PrimFunc.register()    
def ARG_TYPES_COARSE_FIRST(label: str) -> str:
    """
    The coarse grained argument types of a relation label, e.g. per:loc
    """
    output = None
    try:
        relation_def = RELATION_DEFS[label]
        output = f"{relation_def[0][0]}"
    except Exception as e:
        ex = Exception(f"Unknown exception from [ ARG_TYPES_COARSE_FIRST ]: {e}")
        raise(ex)
    else:
        return output

@PrimFunc.register()    
def ARG_TYPES_COARSE_SECOND(label: str) -> str:
    """
    The coarse grained argument types of a relation label, e.g. per:loc
    """
    output = None
    try:
        relation_def = RELATION_DEFS[label]
        output = f"{relation_def[1][0]}"
    except Exception as e:
        ex = Exception(f"Unknown exception from [ ARG_TYPES_COARSE_SECOND ]: {e}")
        raise(ex)
    else:
        return output


def GET_ENTITY_SPANS(ent_types):
    start_idx = 0
    type_spans = []
    for ent_type, group in groupby(ent_types):
        if ent_type == "O":
            start_idx += len(list(group))
            continue

        end_idx = start_idx + len(list(group))
        type_spans.append((ent_type, (start_idx, end_idx)))

        start_idx = end_idx

    return type_spans


@PrimFunc.register()
def COUNT_SAME_ENTITY_IN_CONTEXT(target: Target, arg: str):
    ent_types = [t.ent_type_ for t in target.doc]

    arg_start, arg_end = target.head if arg == "head" else target.tail
    other_start, _ = target.head if arg != "head" else target.tail
    arg_type = ent_types[arg_start]

    if arg_type == "O":
        return -1

    count = 0
    ent_spans = GET_ENTITY_SPANS(ent_types)
    for ent_type, (ent_start, ent_end) in ent_spans:
        if ent_type == arg_type and ent_start != arg_start and ent_start != other_start:
            count += 1    
    return count


@PrimFunc.register()
def COUNT_ENTITY_IN_CONTEXT(target: Target, entity: str = None):
    ent_types = [t.ent_type_ for t in target.doc]

    head_start, _ = target.head
    tail_start, _ = target.tail

    count = 0
    ent_spans = GET_ENTITY_SPANS(ent_types)
    for ent_type, (ent_start, ent_end) in ent_spans:
        if ent_start != head_start and ent_start != tail_start:
            if entity is None or ent_type == entity:
                count += 1
    return count


@PrimFunc.register()
def NUM_DISTRACTOR_BETWEEN_ARGUMENTS(target: Target):
    ent_types = [t.ent_type_ for t in target.doc]

    arg_first = target.head if target.head[0] < target.tail[0] else target.tail
    arg_last = target.head if target.head[0] > target.tail[0] else target.tail
    
    arg_types = set([ent_types[arg_first[0]], ent_types[arg_last[0]]])
    if "O" in arg_types:
        arg_types.remove("O")

    if not arg_types:
        return -1

    count = 0
    ent_spans = GET_ENTITY_SPANS(ent_types)
    for ent_type, (ent_start, ent_end) in ent_spans:
        if ent_type in arg_types and ent_start != arg_first[0] and ent_start != arg_last[0]:
            if arg_first[1] < ent_start < arg_last[0]:
                count += 1
    return count


@PrimFunc.register()
def HAS_INVERSE_RELATION(label: str):
    return label in INVERSE_RELATIONS


@PrimFunc.register()
def INVERSE_LABEL(label: str):
    return INVERSE_RELATIONS.get(label, "NONE")


@PrimFunc.register()
def COARSE_SUBJ_OBJ_TYPE(label: str):
    return TACRED_SUBJ_OBJ_TYPES[label]
