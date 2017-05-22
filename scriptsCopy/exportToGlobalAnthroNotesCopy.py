# coding=utf-8
# import bisect
import uuid
import xml.etree.ElementTree as ET
# import json
import datetime

from unicode_utils import load_unicode_csv_file_rows


def export_csv_to_global_anthro_notes(language='English'):

    orc_char = u"\uFFFC"
    comment_list = ET.Element("CommentList")

    ocms_to_publish = ['203 Dissemination of News and Information', '801 Numerology', '243 Cereal Agriculture',
                       '764 Burial Practices and Funerals', '821 Ethnometeorology', '290 Clothing',
                       '787 Revelation and Divination']
    section_topics_to_publish = ['2 Description', '3 Application to Biblical source', '5 Research Suggestions']

    #csv_rows = unicode_utils.load_unicode_csv_file_rows('scripts/data/anthroNoteContent.csv')
    csv_rows = load_unicode_csv_file_rows('scriptsCopy/data/anthroNoteContent.csv')
    ocm_choice_processing = ''
    increment = 0
    section_topic_processing = ''
    bullet_processing = False
    previously_processed_bullet = False
    for row in csv_rows:
        ocm_choice = row['ocm_choice']
        if not ocm_choice or ocm_choice not in ocms_to_publish:
            continue
        print (unicode(row['refs']), unicode(row['ocm_choice']), unicode(row['¶_content_'+ language]))
        if ocm_choice != ocm_choice_processing:
            ocm_choice_processing = ocm_choice
            thread = str(uuid.uuid4())[:8]
            first_ref = None
            main_comment = create_comment(comment_list, thread, increment, language)
            increment += 1
            contents = ET.SubElement(main_comment, "Contents")
            p = ET.SubElement(contents, "p")
            bold = ET.SubElement(p, "bold")
            #ocm_description = ocm_descriptions.get(ocm['code'])
            #if ocm_description:
            #    bold.tail = " : " + ocm_description['description']
            title = " ".join(ocm_choice.split()[1:])
            ocm_code = ocm_choice.split()[0]
            bold.text = u"{} (OCM {})".format(title, ocm_code)
        section_topic = row['section_topic']
        if section_topic not in section_topics_to_publish:
            continue
        if section_topic != section_topic_processing:
            section_topic_processing = section_topic
            if not previously_processed_bullet:
                # add some extra spacing
                # todo change stylesheet to add margin-bottom to ul?
                p = ET.SubElement(contents, "p")
            previously_processed_bullet = False
            p = ET.SubElement(contents, "p")
            bold = ET.SubElement(p, "bold")
            bold.text = u" ".join(section_topic.split()[1:])
        if not row['¶_content_' + language]:
            continue
        content = unicode(row['¶_content_' + language])
        if row['bullet']:
            if not bullet_processing:
                ul = ET.SubElement(contents, "ul")
                bullet_processing = True
            li = ET.SubElement(ul, "li")
            li.text = content
            previously_processed_bullet = True
            continue
        else:
            bullet_processing = False
        previously_processed_bullet = False
        if section_topic == '3 Application to Biblical source':
            ref = row['refs']
            p = ET.SubElement(contents, "p", attrib={'class': 'scrtext'})
            #span_ref = ET.SubElement(p, "span", attrib={'class': 'verseref'})
            span_ref = ET.SubElement(p, "span")
            span_ref.text = ref
            #span_content = ET.SubElement(p, "span", attrib={'class': 'commentary'})
            span_content = ET.SubElement(p, "span")
            span_content.text = content
            if first_ref is None:
                first_ref = ref
                comment = main_comment
            else:
                reattached_comment = create_comment(comment_list, thread, increment, language, first_ref)
                increment += 1
                comment = reattached_comment
                ET.SubElement(reattached_comment, "Field", Name="reattached").text = orc_char.join([ref, '', str(0), '', ''])
                #reattached_comment.find("VerseRef").text = first_ref
            #comment.find("VerseRef").text = first_ref
            comment.set("VerseRef", first_ref)
            continue
        p = ET.SubElement(contents, "p")
        p.text = content
    tree = ET.ElementTree(comment_list)
    filepath = "scriptsCopy/data/Comments_Global Anthro Demo2017-05-22 {}.xml".format(language)
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    print "Output: " + filepath


def create_comment(comment_list, thread, increment, language, verseRef = ''):
    time = datetime.datetime.now().isoformat()
    time = time[:-1] + str(increment)
    date = time + "-04:00"
    myattributes = {"Thread" : thread, "User" : "Global Anthro Notes", "Date" : date, "VerseRef" : verseRef,
                    "Language" : language }
    '''
    New in version 2.7.

    xml.etree.ElementTree.SubElement(parent, tag, attrib={}, **extra)
    Subelement factory. This function creates an element instance, and appends it to an existing element.
    
    The element name, attribute names, and attribute values can be either bytestrings or Unicode 
    strings. parent is the parent element. tag is the subelement name. attrib is an optional 
    dictionary, containing element attributes. extra contains additional attributes, 
    given as keyword arguments. Returns an element instance.
    '''

    comment = ET.SubElement(comment_list, "Comment", attrib=myattributes )
    #ET.SubElement(comment, "Thread").text = thread
    #ET.SubElement(comment, "User").text = "Global Anthro Notes"
    #ET.SubElement(comment, "VerseRef").text = ''
    ET.SubElement(comment, "StartPosition").text = '0'
    ET.SubElement(comment, "Status").text = ''
    ET.SubElement(comment, "Type").text = ''
    #ET.SubElement(comment, "Language").text = language
    #time = datetime.datetime.now().isoformat()
    #time = time[:-1] + str(increment)
    #ET.SubElement(comment, "Date").text = time + "-04:00"
    return comment

#Sexport_csv_to_global_anthro_notes(language='English')