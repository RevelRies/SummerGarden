from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(3, 10)

    @task(2)
    def get_all_objects(self):
        # получение всех объектов
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                        query getObjects {
                            objects {
                            edges {
                              node {
                                pk
                                name
                                type {
                                  pk
                                  name
                                }
                              }
                            }
                            }
                            }
                    """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)

    @task(1)
    def get_all_objects_order_by_name(self):
        # получение объектов отсортированных по имени
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                    query getObjects {
                        objects (orderBy: "name") {
                        edges {
                          node {
                            pk
                            name
                            type {
                              pk
                              name
                            }
                          }
                        }
                        }
                        }
                    """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)

    @task(1)
    def get_objects_by_type(self):
        # получение объектов по типу
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                        query getObjects {
                            objects (type_Name_Icontains: "скульптура") {
                            edges {
                              node {
                                pk
                                name
                                type {
                                  pk
                                  name
                                }
                              }
                            }
                            }
                            }
                    """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)

    @task(2)
    def get_object_by_name(self):
        # получение объекта по имени
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                    query getObjects {
                        objects (name_Icontains: "сат") {
                        edges {
                          node {
                            pk
                            name
                            type {
                              pk
                              name
                            }
                          }
                        }
                        }
                        }
                    """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)

    @task(5)
    def get_object_by_id(self):
        # получение объекта по id
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                        query getObjects {
                            objects (id: 14) {
                            edges {
                              node {
                                pk
                                name
                                type {
                                  pk
                                  name
                                }
                              }
                            }
                            }
                            }
                        """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)

    @task(1)
    def get_objects_types_order_by_name(self):
        # получение типов отсортированных по имени
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                    query getObjectsTypes {
                      objectTypes (orderBy: "name") {
                        edges {
                          node {
                            pk
                            name
                          }
                        }
                        }
                    }
                    """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)

    @task(1)
    def get_objects_types(self):
        # получение типов объектов
        headers = {'content-type': 'application/json'}
        body = {
            "query": """
                            query getObjectsTypes {
                              objectTypes {
                                edges {
                                  node {
                                    pk
                                    name
                                  }
                                }
                                }
                            }
                            """
        }
        self.client.post("/summer_garden/graphql/", json=body, headers=headers)