import twint
import nest_asyncio

nest_asyncio.apply()

c = twint.Config()

c.Search = 'spiderman'
c.Store_object = True
twint.run.Lookup(c)
user = twint.output.users_list[0]
print(user.avatar)