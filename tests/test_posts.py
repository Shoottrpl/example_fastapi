from typing import List

import pytest

from app import schemas


# def test_get_all_post(authorized_client, create_posts):
#     response = authorized_client.get("/posts")
#
#     def validate(post):
#         return schemas.PostOut(**post)
#
#     map_posts = map(validate, response.json())
#     post_list = list(map_posts)
#
#     assert response.status_code == 200
#     assert len(response.json()) == len(create_posts)
#     assert post_list[0].Post.id == create_posts[0].id
#
#
# def test_unauthorized_user_get_all_posts(client, create_posts):
#     response = client.get("/posts")
#     assert response.status_code == 401
#
#
# def test_unauthorized_user_get_one_posts(client, create_posts):
#     response = client.get(f"/posts/{create_posts[0].id}")
#     assert response.status_code == 401
#
#
# def test_get_one_post_not_exist(authorized_client, create_posts):
#     response = authorized_client.get(f"/posts/444")
#     assert response.status_code == 404
#
#
# def test_get_one_post(authorized_client, create_posts):
#     response = authorized_client.get(f"/posts/{create_posts[0].id}")
#     post = schemas.PostOut(**response.json())
#
#     assert response.status_code == 200
#     assert post.Post.id == create_posts[0].id
#     assert post.Post.title == create_posts[0].title
#     assert post.Post.content == create_posts[0].content
#
# @pytest.mark.parametrize("title, content, published", [
#     ("test1", "test_content_1", True),
#     ("test2", "test_content_2", False),
#     ("test3", "test_content_3", True)
# ])
# def test_create_post(authorized_client, test_user, create_posts, title, content, published):
#     response = authorized_client.post("/posts", json={"title": title, "content": content,
#                                                       "published": published})
#
#     created_post = schemas.Post(**response.json())
#     assert response.status_code == 201
#     assert created_post.title == title
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.user_id == test_user["id"]
#
#
# def test_create_post_default_published_true(authorized_client, test_user, create_posts):
#     response = authorized_client.post(
#         "/posts", json={"title": "test", "content": "test_content"})
#
#     created_post = schemas.Post(**response.json())
#     assert response.status_code == 201
#     assert created_post.title == "test"
#     assert created_post.content == "test_content"
#     assert created_post.published is True
#     assert created_post.user_id == test_user["id"]
#
#
# def test_unauthorized_user_create_posts(client, create_posts):
#     response = client.post(
#         "/posts", json={"title": "test", "content": "test_content"})
#     assert response.status_code == 401
#
#
# def test_unauthorized_user_delete_posts(client, create_posts):
#     response = client.delete(f"/posts/{create_posts[0].id}")
#     assert response.status_code == 401
#
#
# def test_delete_post_success(authorized_client, create_posts):
#     response = authorized_client.delete(f"/posts/{create_posts[0].id}")
#     assert response.status_code == 204
#
#
# def test_delete_post_not_exist(authorized_client, create_posts):
#     response = authorized_client.delete("/posts/444")
#     assert response.status_code == 404
#
#
# def test_delete_other_user_post(authorized_client, test_user, create_posts):
#     response = authorized_client.delete(f"/posts/{create_posts[3].id}")
#     assert response.status_code == 403


def test_update_post_not_exist(authorized_client, test_user, create_posts):
    data = {
        "title": "test",
        "content": "test_content",
        "user_id": test_user["id"]
    }

    response = authorized_client.put(f"/posts/{create_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, create_posts):
    data = {
        "title": "test",
        "content": "test_content",
        "user_id": test_user["id"]
    }

    response = authorized_client.put(f"/posts/{create_posts[3].id}", json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_posts(client, test_user, create_posts):
    response = client.put(f"/posts/{create_posts[0].id}")
    assert response.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, create_posts):
    data = {
        "title": "test",
        "content": "test_content",
        "user_id": test_user["id"]
    }

    response = authorized_client.put("/posts/444", json=data)
    assert response.status_code == 404