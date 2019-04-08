from . import ExchangeTest
from elasticsearch_dsl import connections
from django.conf import settings
from elasticsearch import Elasticsearch
import pytest
from django.core.management import call_command


@pytest.mark.skipif(settings.ES_SEARCH is False,
                    reason="Only run if using unified search")
class GeonodeElasticsearchTest(ExchangeTest):

    def setUp(self):
        super(GeonodeElasticsearchTest, self).setUp()
        self.login()
        call_command('rebuild_index')
        # connect to the ES instance
        connections.create_connection(hosts=[settings.ES_URL])

    def test_management_commands(self):
        es = Elasticsearch(settings.ES_URL)
        mappings = es.indices.get_mapping()

        # Ensure all the indices exist in our mappings upon build
        self.assertTrue('profile-index' in mappings)
        self.assertTrue('layer-index' in mappings)
        self.assertTrue('map-index' in mappings)
        self.assertTrue('document-index' in mappings)
        self.assertTrue('group-index' in mappings)

        # Call the clear command and ensure the indices have been wiped
        call_command('clear_index')
        mappings = es.indices.get_mapping()
        self.assertFalse('profile-index' in mappings)
        self.assertFalse('layer-index' in mappings)
        self.assertFalse('map-index' in mappings)
        self.assertFalse('document-index' in mappings)
        self.assertFalse('group-index' in mappings)

        # Rebuild the indices and ensure they return to our mappings
        call_command('rebuild_index')
        mappings = es.indices.get_mapping()
        self.assertTrue('profile-index' in mappings)
        self.assertTrue('layer-index' in mappings)
        self.assertTrue('map-index' in mappings)
        self.assertTrue('document-index' in mappings)
        self.assertTrue('group-index' in mappings)

    def test_mappings(self):
        # We only want to test mappings because the rest should be covered
        # in the views_test.py for faceting and filtering
        es = Elasticsearch(settings.ES_URL)
        mappings = es.indices.get_mapping()

        profile_mappings = mappings[
            'profile-index']['mappings']['doc']['properties']
        profile_properties = {
            "avatar_100": {
                "type": "text"
            },
            "documents_count": {
                "type": "integer"
            },
            "first_name": {
                "type": "text"
            },
            "id": {
                "type": "integer"
            },
            "last_name": {
                "type": "text"
            },
            "layers_count": {
                "type": "integer"
            },
            "maps_count": {
                "type": "integer"
            },
            "organization": {
                "type": "text"
            },
            "position": {
                "type": "keyword"
            },
            "profile": {
                "type": "keyword"
            },
            "profile_detail_url": {
                "type": "text"
            },
            "type": {
                "type": "keyword",
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                }
            },
            "username": {
                "type": "keyword",
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                }
            },
            "date_joined": {
                "type": "date"
            }
        }

        self.assertDictEqual(profile_mappings, profile_properties)

        group_mappings = mappings[
            'group-index']['mappings']['doc']['properties']
        group_properties = {
            "description": {
                "type": "text"
            },
            "detail_url": {
                "type": "text"
            },
            "id": {
                "type": "integer"
            },
            "json": {
                "type": "text"
            },
            "slug": {
                "type": "text"
            },
            "title": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "pattern": {
                        "analyzer": "pattern_analyzer",
                        "type": "text"
                    }
                },
                "type": "text"
            },
            "title_sortable": {
                "type": "keyword"
            },
            "type": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "last_modified": {
                "type": "date"
            }
        }
        self.assertDictEqual(group_mappings, group_properties)

        document_mappings = mappings[
            'document-index']['mappings']['doc']['properties']
        document_properties = {
            "abstract": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "pattern": {
                        "analyzer": "pattern_analyzer",
                        "type": "text"
                    }
                },
                "type": "text"
            },
            "bbox_bottom": {
                "type": "float"
            },
            "bbox_left": {
                "type": "float"
            },
            "bbox_right": {
                "type": "float"
            },
            "bbox_top": {
                "type": "float"
            },
            "category": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "category__gn_description": {
                "type": "text"
            },
            "csw_type": {
                "type": "keyword"
            },
            "csw_wkt_geometry": {
                "type": "keyword"
            },
            "date": {
                "type": "date"
            },
            "detail_url": {
                "type": "keyword"
            },
            "id": {
                "type": "integer"
            },
            "keywords": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "num_comments": {
                "type": "integer"
            },
            "num_ratings": {
                "type": "integer"
            },
            "owner__username": {
                "fields": {
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "popular_count": {
                "type": "integer"
            },
            "rating": {
                "type": "integer"
            },
            "regions": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "share_count": {
                "type": "integer"
            },
            "srid": {
                "type": "keyword"
            },
            "supplemental_information": {
                "type": "text"
            },
            "temporal_extent_end": {
                "type": "date"
            },
            "temporal_extent_start": {
                "type": "date"
            },
            "thumbnail_url": {
                "type": "keyword"
            },
            "title": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "pattern": {
                        "analyzer": "pattern_analyzer",
                        "type": "text"
                    }
                },
                "type": "text"
            },
            "title_sortable": {
                "type": "keyword"
            },
            "type": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "uuid": {
                "type": "keyword"
            },
            # GVS custom facet fields
            "license": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            }
        }
        self.assertDictEqual(document_mappings, document_properties)

        layer_mappings = mappings[
            'layer-index']['mappings']['doc']['properties']
        layer_properties = {
            "rating": {
                "type": "integer"
            },
            "owner__last_name": {
                "type": "text"
            },
            "has_time": {
                "type": "boolean"
            },
            "bbox_top": {
                "type": "float"
            },
            "category__gn_description": {
                "type": "text"
            },
            "temporal_extent_end": {
                "type": "date"
            },
            "abstract": {
                "fields": {
                    "pattern": {
                        "type": "text",
                        "analyzer": "pattern_analyzer"
                    },
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    }
                },
                "type": "text"
            },
            "srid": {
                "type": "keyword"
            },
            "bbox_bottom": {
                "type": "float"
            },
            "bbox_right": {
                "type": "float"
            },
            "keywords": {
                "fields": {
                    "text": {
                        "type": "text"
                    },
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    }
                },
                "type": "keyword"
            },
            "featured": {
                "type": "boolean"
            },
            "thumbnail_url": {
                "type": "keyword"
            },
            "references": {
                "properties": {
                    "url": {
                        "type": "text"
                    },
                    "scheme": {
                        "fields": {
                            "pattern": {
                                "type": "text",
                                "analyzer": "pattern_analyzer"
                            },
                            "text": {
                                "type": "text"
                            }
                        },
                        "type": "keyword"
                    },
                    "name": {
                        "fields": {
                            "text": {
                                "type": "text"
                            }
                        },
                        "type": "keyword"
                    }
                }
            },
            "type": {
                "fields": {
                    "text": {
                        "type": "text"
                    },
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    }
                },
                "type": "keyword"
            },
            "date": {
                "type": "date"
            },
            "owner__first_name": {
                "type": "text"
            },
            "detail_url": {
                "type": "keyword"
            },
            "id": {
                "type": "integer"
            },
            "category": {
                "fields": {
                    "text": {
                        "type": "text"
                    },
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    }
                },
                "type": "keyword"
            },
            "num_ratings": {
                "type": "integer"
            },
            "uuid": {
                "type": "keyword"
            },
            "title": {
                "fields": {
                    "pattern": {
                        "type": "text",
                        "analyzer": "pattern_analyzer"
                    },
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    }
                },
                "type": "text"
            },
            "num_comments": {
                "type": "integer"
            },
            "title_sortable": {
                "type": "keyword"
            },
            "supplemental_information": {
                "type": "text"
            },
            "bbox_left": {
                "type": "float"
            },
            "temporal_extent_start": {
                "type": "date"
            },
            "regions": {
                "fields": {
                    "text": {
                        "type": "text"
                    },
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    }
                },
                "type": "keyword"
            },
            "subtype": {
                "fields": {
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "source_host": {
                "fields": {
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "csw_type": {
                "type": "keyword"
            },
            "typename": {
                "type": "keyword"
            },
            "csw_wkt_geometry": {
                "type": "keyword"
            },
            "share_count": {
                "type": "integer"
            },
            "owner__username": {
                "fields": {
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "popular_count": {
                "type": "integer"
            },
            "geogig_link": {
                "type": "keyword"
            },
            "is_published": {
                "type": "boolean"
            },
            # GVS custom facet fields
            "license": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "classification": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "caveat": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "provenance": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "poc_name": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            }
        }
        self.assertDictEqual(layer_mappings, layer_properties)

        map_mappings = mappings[
            'map-index']['mappings']['doc']['properties']
        map_properties = {
            "abstract": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "pattern": {
                        "analyzer": "pattern_analyzer",
                        "type": "text"
                    }
                },
                "type": "text"
            },
            "bbox_bottom": {
                "type": "float"
            },
            "bbox_left": {
                "type": "float"
            },
            "bbox_right": {
                "type": "float"
            },
            "bbox_top": {
                "type": "float"
            },
            "category": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "category__gn_description": {
                "type": "text"
            },
            "csw_type": {
                "type": "keyword"
            },
            "csw_wkt_geometry": {
                "type": "keyword"
            },
            "date": {
                "type": "date"
            },
            "detail_url": {
                "type": "keyword"
            },
            "id": {
                "type": "integer"
            },
            "keywords": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "num_comments": {
                "type": "integer"
            },
            "num_ratings": {
                "type": "integer"
            },
            "owner__username": {
                "fields": {
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "popular_count": {
                "type": "integer"
            },
            "rating": {
                "type": "integer"
            },
            "regions": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "share_count": {
                "type": "integer"
            },
            "srid": {
                "type": "keyword"
            },
            "supplemental_information": {
                "type": "text"
            },
            "temporal_extent_end": {
                "type": "date"
            },
            "temporal_extent_start": {
                "type": "date"
            },
            "thumbnail_url": {
                "type": "keyword"
            },
            "title": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "pattern": {
                        "analyzer": "pattern_analyzer",
                        "type": "text"
                    }
                },
                "type": "text"
            },
            "title_sortable": {
                "type": "keyword"
            },
            "type": {
                "fields": {
                    "english": {
                        "analyzer": "english",
                        "type": "text"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            },
            "uuid": {
                "type": "keyword"
            },
            # GVS custom facet fields
            "license": {
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "text": {
                        "type": "text"
                    }
                },
                "type": "keyword"
            }
        }
        self.assertDictEqual(map_mappings, map_properties)
