import gitlab


def siemens():
    siemens_project_id = 154395
    siemens_url = "https://code.siemens.com/walter%2Emarchewka%2Ftest1"
    siemens_private_token = 'CSC-L6_1YCs8kzvHxVETtDnt'
    siemens_connection = gitlab.Gitlab('https://code.siemens.com/', private_token='{}'.format(siemens_private_token))

    siemens_all_projects = siemens_connection.projects.list(owned=True)
    print(siemens_all_projects)

    siemens_project = siemens_connection.projects.get(siemens_project_id)
    print(siemens_project.name)

    # siemens_attr_list = siemens_project.customattributes.list()
    # print(siemens_attr_list)

    siemens_bte_group_id = 77349
    siemens_new_project = siemens_connection.projects.create(
        {'name': 'bte_test_1', 'namespace_id': siemens_bte_group_id, 'visibility': 'private'})


def git_lab():
    gitlab_project_id = 23596290
    gitlab_url = "https://gitlab.com/siemensbte"
    gitlab_private_token = 'zX3Sz3_-3XadLdHqD_tR'
    gitlab_connection = gitlab.Gitlab('https://gitlab.com/', private_token='{}'.format(gitlab_private_token))

    gitlab_all_projects = gitlab_connection.projects.list(owned=True)
    print(gitlab_all_projects)

    gitlab_project = gitlab_connection.projects.get(gitlab_project_id)
    print(gitlab_project.name)

    gitlab_groups = gitlab_connection.groups.list()
    print(gitlab_groups)

    gitlab_group = gitlab_connection.groups.get(10603075)
    print(gitlab_group)

    # gitlab_group_attr_list = gitlab_group.customattributes.list()
    # print(gitlab_group_attr_list)
    #


if __name__ == '__main__':
    siemens()
    # git_lab()

# attr = project.customattributes.get('')
# try:
#     status = gitlab_connection.projects.delete(url)
# except Exception as e:
#     print("ERROR:{}".format(e))
# all_projects = gitlab_connection.projects.list(owned=True)
# for project in all_projects:
#     name = project.name
#     id = project.id
#     try:
#         status = gitlab_connection.projects.delete(id)
#     except Exception as e:
#         print("ERROR:{}".format(e))
