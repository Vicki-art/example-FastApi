
def test_vote_for_post(authorized_client, test_posts): 
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 201 

def test_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote): 
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 201

def test_delete_vote_not_exist(authorized_client, test_posts): 
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[2].id, "dir": 0})

    assert res.status_code == 404

def test_vote_not_exist_post(authorized_client, test_posts): 
    res = authorized_client.post("/vote/", json = {"post_id": 8000, "dir": 1})

    assert res.status_code == 404

def test_vote_not_authorized(client, test_posts): 
    res = client.post("/vote/", json = {"post_id": test_posts[2].id, "dir": 1})

    assert res.status_code == 401

