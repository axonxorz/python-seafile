#coding: UTF-8

import pytest

from seafileapi.exceptions import DoesNotExist
from tests.utils import randstring

def test_create_delete_repo(client):
    repo = _create_repo(client)
    repo.delete()

    with pytest.raises(DoesNotExist):
        client.repos.get_repo(repo.id)

def test_create_encrypted_repo(client):
    repo = _create_repo(client, password=randstring())
    repo.delete()
    with pytest.raises(DoesNotExist):
        client.repos.get_repo(repo.id)

def test_list_repos(client):
    repos = client.repos.list_repos()
    for repo in repos:
        print(repo.name, ":", repo.owner)
        assert len(repo.id) == 36

def test_list_shared_folder(client):
    repos = client.repos.list_shared_folders()
    for repo in repos:

        print(repo)

def test_shared_folder_to_user(client):
    repo_obj = client.repos.get_repo_by_name("temp_bak")
    param = {"path":"/新车sd88发布", "share_type":"user", "users":"1051708338@qq.com", "group_id":None, "permission":'rw'}
    repo_obj.share_folder(**param)

def test_unshared_folder_to_user(client):
    repo_obj = client.repos.get_repo_by_name("temp_bak")
    param = {"path":"/1", "share_type":"user", "users":"1051708338@qq.com", "group_id":None, "permission":'rw'}
    repo_obj.unshare_folder(**param)

def test_is_exist_dir(client):

    repo_obj = client.repos.get_repo_by_name("temp_bak")
    assert repo_obj.is_exist_dir("/1") == True
    assert repo_obj.is_exist_dir("/x1") == False






def _create_repo(client, password=None):
    repo_name = '测试资料库-%s' % randstring()
    repo_desc = '一个测试资料库-%s' % randstring()
    repo = client.repos.create_repo(repo_name, repo_desc, password=password)

    assert repo.name == repo_name
    assert repo.desc == repo_desc
    assert len(repo.id) == 36
    assert repo.encrypted == (password is not None)
    assert repo.owner == 'self'

    return repo
