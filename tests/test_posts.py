import pytest
from app import schemas 

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    print(list(posts_map))
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_not_authorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401

def test_not_authorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_non_existing_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888")

    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
                         ("my favourite pizza", "pepperoni", True), 
                         ("my favourite flower", "rose", False), 
                         ("my favourite weather", "sunny", True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json = {'title': title, 
                                'content': content, 'published': published})
    new_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert new_post.title == title 
    assert new_post.content == content 
    assert new_post.published == published 

def test_create_post_defualt_published(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json = {'title': "arbitary title", 
                                'content': 'arbitary content'})
    new_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert new_post.title == "arbitary title" 
    assert new_post.content == "arbitary content" 
    assert new_post.published == True 

def test_not_authorized_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json = {'title': "arbitary title", 
                                'content': 'arbitary content'})
    assert res.status_code == 401

def test_not_authorized_delete_post(client , test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_authorized_delete_not_existing_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/80000")
    assert res.status_code == 404

def test_authorized_delete_post_owned_bu_another_user(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post_authorized(authorized_client, test_user, test_posts):
    data = {"title": "update title", "content": "update content"}
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json = data)

    updated_post = schemas.PostBase(**res.json())
    assert res.status_code == 200
    assert updated_post.title == "update title"
    assert updated_post.content ==  "update content"
    assert updated_post.published == True 

def test_update_post_not_authorized(client, test_user, test_posts):
    data = {"title": "update title", "content": "update content"}
    res = client.put(f"/posts/{test_posts[2].id}", json = data)

    assert res.status_code == 401


def test_update_post_authorized_delete_wrong_post(authorized_client, test_user, test_user2, test_posts):
    data = {"title": "update title", "content": "update content"}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)

    assert res.status_code == 403


def test_update_not_existing_post_authorized(authorized_client, test_user, test_posts):
    data = {"title": "update title", "content": "update content"}
    res = authorized_client.put(f"/posts/8000", json = data)

    assert res.status_code == 404
