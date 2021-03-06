import graphene
import hashlib
import binascii

from .models import User, Playlist, Genre, Epoch, Artist, Release, Composition, Track


# class ProductSchema(graphene.ObjectType):
#     name = graphene.String()
#     brand = graphene.String()
#     category = graphene.String()
#
#     price = graphene.Float()
#     amount = graphene.Int()
#
#
# class ProductInput(graphene.InputObjectType):
#     name = graphene.String(required=True)
#     price = graphene.Float(required=True)
#     amount = graphene.Int(required=True)
#
#
# class StoreSchema(graphene.ObjectType):
#     name = graphene.String()
#     address = graphene.String()
#
#     products = graphene.List(ProductSchema)
#
#     def __init__(self, **kwargs):
#         self._id = kwargs.pop('_id')
#         super().__init__(**kwargs)
#
#     def resolve_products(self, info):
#         return [ProductSchema(**product) for product in Store().fetch(self._id).fetch_products()]
#
#
# class StoreInput(graphene.InputObjectType):
#     name = graphene.String(required=True)
#     address = graphene.String(required=True)
#
#
# class ReceiptSchema(graphene.ObjectType):
#     total_amount = graphene.Float()
#     timestamp = graphene.String()
#
#     products = graphene.List(ProductSchema)
#
#     def __init__(self, **kwargs):
#         self._id = kwargs.pop('_id')
#         super().__init__(**kwargs)
#
#     def resolve_products(self, info):
#         return [ProductSchema(**product) for product in Receipt().fetch(self._id).fetch_products()]
#
#
# class SubmitReceipt(graphene.Mutation):
#     class Arguments:
#         customer_email = graphene.String(required=True)
#         products = graphene.List(graphene.NonNull(ProductInput))
#         store = StoreInput(required=True)
#         timestamp = graphene.String(required=True)
#
#     success = graphene.Boolean()
#
#     def mutate(self, info, **kwargs):
#         customer = Customer(email=kwargs.pop('customer_email')).fetch()
#         customer.submit_receipt(**kwargs)
#
#         return SubmitReceipt(success=True)
#
#
# class CustomerSchema(graphene.ObjectType):
#     email = graphene.String()
#     name = graphene.String()
#
#     stores = graphene.List(StoreSchema)
#     receipts = graphene.List(ReceiptSchema)
#     products = graphene.List(ProductSchema)
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.customer = Customer(email=self.email).fetch()
#
#     def resolve_stores(self, info):
#         return [StoreSchema(**store.as_dict()) for store in self.customer.stores]
#
#     def resolve_receipts(self, info):
#         return [ReceiptSchema(**receipt.as_dict()) for receipt in self.customer.receipts]
#
#     def resolve_products(self, info):
#         return [ProductSchema(**product.as_dict()) for product in self.customer.products]
#
#
# class CreateCustomer(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         email = graphene.String(required=True)
#
#     success = graphene.Boolean()
#     customer = graphene.Field(lambda: CustomerSchema)
#
#     def mutate(self, info, **kwargs):
#         customer = Customer(**kwargs)
#         customer.save()
#
#         return CreateCustomer(customer=customer, success=True)
#
#
# class Query(graphene.ObjectType):
#     customer = graphene.Field(lambda: CustomerSchema, email=graphene.String())
#     stores = graphene.List(lambda: StoreSchema)
#     products = graphene.List(lambda: ProductSchema)
#
#     def resolve_customer(self, info, email):
#         customer = Customer(email=email).fetch()
#         return CustomerSchema(**customer.as_dict())
#
#     def resolve_stores(self, info):
#         return [StoreSchema(**store.as_dict()) for store in Store().all]
#
#     def resolve_products(self, info):
#         return [ProductSchema(**product.as_dict()) for product in Product().all]
#
#
# class Mutations(graphene.ObjectType):
#     create_customer = CreateCustomer.Field()
#     submit_receipt = SubmitReceipt.Field()
#


class UserSchema(graphene.ObjectType):
    username = graphene.String()
    email = graphene.String()

    friends = graphene.List(lambda: UserSchema)
    playlists = graphene.List(lambda: PlaylistSchema)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._user = None

    @property
    def user(self):
        if not self._user:
            self._user = User(username=self.username).fetch()
        return self._user

    def resolve_friends(parent, info):
        return [UserSchema(**user.as_dict()) for user in parent.user.friends]

    def resolve_playlists(parent, info):
        return [PlaylistSchema(**playlist.as_dict()) for playlist in parent.user.playlists]


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserSchema)

    def mutate(parent, info, username, password, email=None):
        h = hashlib.md5(password.encode())
        password = binascii.hexlify(h.digest()).decode()

        user = User(username=username, password=password, email=email)
        user.save()

        return CreateUser(user=user, ok=True)

# =============================================================================

class PlaylistSchema(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()


# =============================================================================


class Query(graphene.ObjectType):
    user = graphene.Field(lambda: UserSchema, username=graphene.String())
    all_users = graphene.Field(lambda: UserSchema)

    def resolve_user(parent, info, username):
        user = User.fetch(username)
        return UserSchema(**user.as_dict())

    def resolve_all_users(parent, info):
        return [UserSchema(**user.as_dict()) for user in User.all()]


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
