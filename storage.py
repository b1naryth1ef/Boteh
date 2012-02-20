import goatfish, sqlite3, cPickle

class Field(goatfish.Model):
    class Meta:
        connection = sqlite3.connect("data.db")
        indexes = (
            ("name", "data"),
        )

Field.initialize()

# testy = {
# 	'a':1,
# 	'b':2
# }

# f = Field()
# f.name = 'Testing Dict'
# f.data = cPickle.dumps(testy, cPickle.HIGHEST_PROTOCOL)
# f.save()

# print [cPickle.loads(test.data) for test in Field.find({'name':'Testing Dict'})]