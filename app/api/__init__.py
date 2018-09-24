from app.api.bootstrap import api
from app.api.geokrety import GeokretDetail, GeokretList, GeokretRelationship
from app.api.geokrety_types import (GeokretTypeDetail, GeokretTypeList,
                                    GeokretTypeRelationship)
from app.api.moves import MoveDetail, MoveRelationship, MovesList
from app.api.moves_types import MovesTypeDetail, MovesTypeList
from app.api.news import NewsDetail, NewsList, NewsRelationship
from app.api.news_comments import (NewsCommentDetail, NewsCommentList,
                                   NewsCommentRelationship)
from app.api.news_subscriptions import (NewsSubscriptionDetail,
                                        NewsSubscriptionList,
                                        NewsSubscriptionRelationship)
from app.api.users import UserDetail, UserList, UserRelationship

api.route(UserList, 'users_list',
          '/users',
          )
api.route(UserDetail,
          'user_details',
          '/users/<int:id>',
          '/news/<int:news_author_id>/author',
          '/news-comments/<int:newscomment_id>/author',
          '/news-subscriptions/<int:news_subscription_id>/user',
          '/geokrety/<int:geokret_owned_id>/owner',
          '/geokrety/<int:geokret_held_id>/holder',
          '/move/<int:move_author_id>/author',
          )
api.route(UserRelationship, 'user_news', '/users/<int:id>/relationships/news')
api.route(UserRelationship, 'user_news_comments', '/users/<int:id>/relationships/news-comments')
api.route(UserRelationship, 'user_geokrety_owned', '/users/<int:id>/relationships/geokrety-owned')
api.route(UserRelationship, 'user_geokrety_held', '/users/<int:id>/relationships/geokrety-held')

api.route(NewsList, 'news_list',
          '/news',
          '/users/<int:author_id>/news',
          )
api.route(NewsDetail, 'news_details',
          '/news/<int:id>',
          '/news-comments/<int:news_comment_id>/news',
          '/news-subscriptions/<int:news_subscription_id>/news',
          )
api.route(NewsRelationship, 'news_comments', '/news/<int:id>/relationships/news-comments')
api.route(NewsRelationship, 'news_author', '/news/<int:id>/relationships/author')
api.route(NewsRelationship, 'news_news_subscription', '/news/<int:id>/relationships/author')

api.route(NewsCommentList, 'news_comments_list',
          '/news-comments',
          '/users/<int:author_id>/news-comments',
          '/news/<int:news_id>/news-comments')
api.route(NewsCommentDetail, 'news_comment_details',
          '/news-comments/<int:id>',
          )
api.route(NewsCommentRelationship, 'news_comments_author', '/news-comments/<int:id>/relationships/author')
api.route(NewsCommentRelationship, 'news_comments_news', '/news-comments/<int:id>/relationships/news')

api.route(NewsSubscriptionList, 'news_subscriptions_list',
          '/news-subscriptions',
          '/users/<int:user_id>/news-subscriptions',
          '/news/<int:news_id>/news-subscriptions')
api.route(NewsSubscriptionDetail, 'news_subscription_details',
          '/news-subscriptions/<int:id>',
          )
api.route(NewsSubscriptionRelationship, 'news_subscription_user', '/news-subscriptions/<int:id>/relationships/user')
api.route(NewsSubscriptionRelationship, 'news_subscription_news', '/news-subscriptions/<int:id>/relationships/news')

api.route(MovesTypeList, 'moves_type_list',
          '/moves-types',
          )
api.route(MovesTypeDetail, 'move_type_details',
          '/moves-types/<int:id>',
          )

api.route(GeokretTypeList, 'geokrety_type_list',
          '/geokrety-types',
          )
api.route(GeokretTypeDetail, 'geokrety_type_details',
          '/geokrety-types/<int:id>',
          '/geokrety/<int:geokret_id>/type',
          )
api.route(GeokretTypeRelationship, 'geokrety_type_geokret', '/geokrety-types/<int:id>/relationships/geokrety')

api.route(GeokretList, 'geokrety_list', '/geokrety',
          '/users/<int:owner_id>/geokrety-owned',
          '/users/<int:holder_id>/geokrety-held',
          '/geokrety-types/<int:geokrety_type_id>/geokrety',
          )
api.route(GeokretDetail, 'geokret_details',
          '/geokrety/<int:id>',
          )
api.route(GeokretRelationship, 'geokret_owner', '/geokrety/<int:id>/relationships/owner')
api.route(GeokretRelationship, 'geokret_holder', '/geokrety/<int:id>/relationships/holder')
api.route(GeokretRelationship, 'geokret_type', '/geokrety/<int:id>/relationships/type')

api.route(
    MovesList,
    'moves_list',
    '/moves',
    '/geokrety/<int:geokret_id>/moves',
)
api.route(
    MoveDetail,
    'move_details',
    '/moves/<int:id>'
)
api.route(MoveRelationship, 'move_geokret', '/geokrety/<int:id>/relationships/moves')
api.route(MoveRelationship, 'move_author', '/moves/<int:id>/relationships/author')
api.route(MoveRelationship, 'move_type', '/moves/<int:id>/relationships/type')
