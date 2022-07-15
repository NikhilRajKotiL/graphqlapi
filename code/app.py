from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.postgresql as postgresql
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_header_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required
)

# initializing our app
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'warp'
app.config["JWT_SECRET_KEY"] = "Warp"

#auth
auth = GraphQLAuth(app)


# Configs

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nikhil@localhost:5432/warp'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
# Modules
db = SQLAlchemy(app)

# Models
class Warp_user_profile(db.Model):
    __tablename__ = 'warp_user_profile'

    user_id = db.Column(postgresql.VARCHAR(10), primary_key=True)
    personaldata_jsonb = db.Column(postgresql.JSONB, nullable = False)
    capacity = db.Column(postgresql.NUMERIC, nullable=False)
    skills = db.Column(postgresql.TEXT, nullable=False)
    interests = db.Column(postgresql.TEXT, nullable=False)
    about_me = db.Column(postgresql.TEXT, nullable=False)
    prof_aspirations = db.Column(postgresql.TEXT, nullable=False)
    target_job_func = db.Column(postgresql.TEXT, nullable=False)
    travel_ready = db.Column(postgresql.BOOLEAN, default = False)
    relocation_outside = db.Column(postgresql.BOOLEAN, default=False)
    relocation_inside = db.Column(postgresql.BOOLEAN, default=False)
    profile_headline = db.Column(postgresql.TEXT, nullable=False)
    education_jsonb = db.Column(postgresql.JSONB, nullable=False)
    experience_jsonb = db.Column(postgresql.JSONB, nullable=False)
    language_jsonb = db.Column(postgresql.JSONB, nullable=False)
    certificates = db.Column(postgresql.BOOLEAN, default=False)
    cert_jsonb = db.Column(postgresql.JSONB)
    status_visible = db.Column(postgresql.BOOLEAN,default=False)
    email_newmsg = db.Column(postgresql.BOOLEAN, default=False)
    email_rolerec = db.Column(postgresql.BOOLEAN, default=False)
    email_reminders = db.Column(postgresql.BOOLEAN, default=False)
    email_vis = db.Column(postgresql.BOOLEAN, default=False)
    phone_vis = db.Column(postgresql.BOOLEAN, default=False)
    mobile_vis = db.Column(postgresql.BOOLEAN, default=False)
    updated_on = db.Column(postgresql.TIMESTAMP)
    created_on = db.Column(postgresql.TIMESTAMP)
    profile_pic = db.Column(postgresql.VARCHAR(256))

    def __repr__(self):
        return '' %self.user_id %self.personaldata_jsonb %self.capacity %self.skills %self.interests %self.about_me %self.prof_aspirations %self.target_job_func %self.travel_ready %self.relocation_outside %self.relocation_inside %self.profile_headline %self.education_jsonb %self.experience_jsonb %self.language_jsonb %self.certificates %self.cert_jsonb %self.status_visible %self.email_newmsg %self.email_rolerec %self.email_reminders %self.email_vis %self.phone_vis %self.mobile_vis %self.updated_on %self.created_on %self.profile_pic

class Warp_user_role(db.Model):
    __tablename__ = 'warp_user_role'

    user_id = db.Column(postgresql.VARCHAR(10), primary_key=True)
    project_id = db.Column(postgresql.INTEGER, primary_key=True)
    role_name = db.Column(postgresql.VARCHAR(50), primary_key=True)
    category = db.Column(postgresql.VARCHAR(20), nullable=False)
    status = db.Column(postgresql.BOOLEAN, nullable=False,default=True)
    updated_on = db.Column(postgresql.TIMESTAMP)
    created_on = db.Column(postgresql.TIMESTAMP)

    def __repr__(self):
        return '' % self.user_id % self.project_id % self.role_name % self.category % self.status % self.updated_on % self.created_on

class User_login(db.Model):
    __tablename__ = 'user_login'

    user_name = db.Column(postgresql.VARCHAR(20), primary_key=True)
    password = db.Column(postgresql.VARCHAR(20),nullable=False)

    def __repr__(self):
        return ''% self.user_name % self.password

class WarpuserprofileObject(SQLAlchemyObjectType):
    class Meta:
         model = Warp_user_profile
         interfaces = (graphene.relay.Node, )    

class WarpuserroleObject(SQLAlchemyObjectType):
    class Meta:
        model = Warp_user_role
        interfaces = (graphene.relay.Node, )

class UserloginObject(SQLAlchemyObjectType):
    class Meta:
        model = User_login
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    user_profile = SQLAlchemyConnectionField(WarpuserprofileObject)
    user_role = SQLAlchemyConnectionField(WarpuserroleObject)
    User_profile = graphene.Field(WarpuserprofileObject, user_id=graphene.String())
    User_role = graphene.Field(WarpuserroleObject, user_id=graphene.String(),project_id=graphene.Int())

    @query_header_jwt_required
    def resolve_User_profile(root,info,user_id):
        return Warp_user_profile.query.filter_by(user_id=user_id).first()

    @query_header_jwt_required
    def resolve_User_role(root,info,user_id,project_id):
        return Warp_user_role.query.filter_by(user_id=user_id,project_id=project_id).first()


# Authentication Mutation
class AuthMutation(graphene.Mutation):
    access_token = graphene.String()

    class Arguments:
        user_name = graphene.String()
        password = graphene.String()
        
    def mutate(self, info, user_name, password):
        user = User_login.query.filter_by(user_name=user_name,password=password).first()
        if not user:
            raise Exception('Authentication Failure : User is not registered')
        return AuthMutation(access_token = create_access_token(identity=user_name))

class Mutation(graphene.ObjectType):
    auth = AuthMutation.Field()

# Schema Objects
schema = graphene.Schema(query=Query, mutation=Mutation)

# Routes
app.add_url_rule(
    '/graphql-api',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.route('/')
def index():
    return 'Welcome to Book Store Api'
if __name__ == '__main__':
     app.run()
