import json

RELATIONSHIP_MAP = {
    ("gene", "mRNA"): "transcribes",
    ("mRNA", "three_prime_UTR"): "contains",
    ("mRNA", "CDS"): "translates",
    ("mRNA", "exon"): "contains",
    ("mRNA", "five_prime_UTR"): "contains",
    ('miRNA', 'exon'): "contains",
    ("ncRNA_gene", "ncRNA"): "transcribes",
    ("ncRNA_gene", "lnc_RNA"): "transcribes",
    ('ncRNA_gene', 'miRNA'): "transcribes",
    ('ncRNA_gene', 'tRNA'): "transcribes",
    ('ncRNA_gene', 'snoRNA'): "transcribes",
    ('ncRNA_gene', 'snRNA'): "transcribes",
    ('ncRNA_gene', 'rRNA'): "transcribes",
    ("lnc_RNA", "exon"): "contains",
    ("ncRNA", "exon"): "contains",
    ('tRNA', 'exon'): "contains",
    ('snoRNA', 'exon'): "contains",
    ('snRNA', 'exon'): "contains",
    ('rRNA', 'exon'): "contains",
}


def get_entity_id_from_gff3_feature(feat):
    attributes = feat.attribs
    if 'ID' in attributes:
        return attributes['ID']
    feat_type = feat.get_type()
    if feat_type + "_id" in attributes:
        return attributes[feat_type + "_id"]
    if feat_type == 'mRNA':
        return attributes["transcript_id"]
    # Fall back on organism, chr, start, end
    return f'{feat.get_source().decode()}_{feat.get_seqid()}:{feat.get_start()}-{feat.get_end()}_{feat.get_type()}'


def create_entity_output(entity):
    entity_id = get_entity_id_from_gff3_feature(entity)
    entity_dict = {"entity_type": entity.get_type(), "entity_id": entity_id, **entity.attribs}
    return entity_id, json.dumps(entity_dict) + '\n'


def create_relationship_output(child, parent):
    child_id = get_entity_id_from_gff3_feature(child)
    parent_id = get_entity_id_from_gff3_feature(parent)
    relationship_dict = {
        "source": parent_id,
        "target": child_id,
        "type": RELATIONSHIP_MAP[(parent.get_type(), child.get_type())]
    }
    return (parent_id, child_id), json.dumps(relationship_dict) + '\n'


def transform_feature_recursive(node, entities_sink, relationships_sink):
    seen_entities = set()
    seen_relationships = set()

    def func(feature, parent=None):
        entity_id, entity_str = create_entity_output(feature)
        if entity_id not in seen_entities:
            entities_sink.write(entity_str)
        for child in feature.traverse_direct():
            relationship_id, relationship_str = create_relationship_output(child, feature)
            if relationship_id not in seen_relationships:
                relationships_sink.write(relationship_str)
            # TODO: Check this is tail recursive and make it so if not
            func(child, feature)

    return func(node)


