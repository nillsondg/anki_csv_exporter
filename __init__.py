from anki.exporting import Exporter
from anki.hooks import addHook
from anki.lang import _
from anki.utils import ids2str, splitFields
import csv
import codecs


class CSVNoteExporter(Exporter):
    key = _("Notes in CSV format")
    ext = ".csv"
    db_query = """
select guid, flds, tags from notes
where id in
(select nid from cards
where cards.id in %s)
	"""

    def __init__(self, col):
        super().__init__(col)
        self.includeTags = True
        # self.includeID = False

    # Overwrite exportInto from Exporter to not open in BufferedIO Mode
    def exportInto(self, path):
        self._escapeCount = 0
        file = codecs.open(path, "w", encoding="utf-8")
        self.doExport(file)
        file.close()

    def doExport(self, file):

        writer = csv.writer(file)
        cardIds = self.cardIds()
        self.count = 0
        for _id, flds, tags in self.col.db.execute(self.db_query % ids2str(cardIds)):
            row = []
            # note id
            # if self.includeID:
            #    row.append(str(_id))
            # fields
            row.extend([self.escapeText(f) for f in splitFields(flds)])
            # tags
            if self.includeTags:
                row.append(tags.strip())
            self.count += 1
            writer.writerow([x for x in row])


def update_exporters_list(exps):
    exps.append(("Notes in CSV format (*.csv)", CSVNoteExporter))


addHook("exportersList", update_exporters_list)
