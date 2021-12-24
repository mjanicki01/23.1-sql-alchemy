from models import Users, Posts, Tags, PostsTags, db
from app import app

db.drop_all()
db.create_all()

j_shmo = Users(first_name = 'Joe', last_name = 'Shmo')
b_brown = Users(first_name = 'Bill', last_name = 'Brown')
k_salad = Users(first_name = 'Kale', last_name = 'Salad', img_url = "https://static.wikia.nocookie.net/theforest_gamepedia/images/5/5d/LeafFarket.png/revision/latest/scale-to-width-down/250?cb=20170924102207")
r_sullivan = Users(first_name = 'Richard', last_name = 'Sullivan', img_url = "https://www.hollywoodreporter.com/wp-content/uploads/2014/01/gene_simmons_headshot_a_p.jpg")

p1 = Posts(title="This is a title", content="This is some content", creator_id=2)
p2 = Posts(title="How to make a PB&J sandwich", content="Call mom", creator_id=3)
p3 = Posts(title="Pandas", content="Eat a lot of bamboo", creator_id=2)
p4 = Posts(title="Favorite book list", content="Too many to fit on one page", creator_id=1)
p5 = Posts(title="Favorite snacks", content="Too many to fit on one page", creator_id=2)
p6 = Posts(title="Another post", content="With some more content", creator_id=3)

t1 = Tags(name="Funny")
t2 = Tags(name="Cooking")
t3 = Tags(name="Recommendations")

db.session.add_all([j_shmo, b_brown, k_salad, r_sullivan, 
p1, p2, p3, p4, p5, p6, 
t1, t2, t3])
db.session.commit()

pt1 = PostsTags(post_id=1, tag_id=3)
pt2 = PostsTags(post_id=2, tag_id=2)
pt3 = PostsTags(post_id=3, tag_id=1)
pt4 = PostsTags(post_id=3, tag_id=2)
pt5 = PostsTags(post_id=4, tag_id=3)
pt6 = PostsTags(post_id=5, tag_id=2)
pt7 = PostsTags(post_id=5, tag_id=3)


db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7])
db.session.commit()