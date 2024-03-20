from datetime import datetime

from pymongo import ReturnDocument

from database import database, Collections


class Users:
    """
    Class to represent a user model to interact with the database
    """

    @classmethod
    def find_one(self, query, reject):
        """
        Method to find a user by a query and reject some fields

        :param query: The query to find the user
        :type query: dict

        :param reject: The fields to reject
        :type reject: dict

        :return: The user found if exists or None
        """
        return database[Collections.USERS].find_one(query, reject)
    

    @classmethod
    def find(self, query, reject):
        """
        Method to find users by a query and reject some fields

        :param query: The query to find the users
        :type query: dict

        :param reject: The fields to reject
        :type reject: dict

        :return: The users found if exists or None
        """
        return database[Collections.USERS].find(query, reject)
    

    @classmethod
    def insert_one(self, user_data):
        """
        Method to insert a user

        :param user: The user to insert
        :type user: dict

        :return: The user inserted
        """
        create_user = database[Collections.USERS].insert_one(user_data)

        if create_user:
            return create_user.id
        
        return False


    @classmethod
    def update_one(self, query, update):
        """
        Method to update a user

        :param query: The query to find the user
        :type query: dict

        :param update: The update to apply
        :type update: dict

        :return: The user updated
        """
        return database[Collections.USERS].find_one_and_update(
            query,
            update,
            return_document=ReturnDocument.AFTER,
        )
    

    @classmethod
    def update_many(self, query, update):
        """
        Method to update users

        :param query: The query to find the users
        :type query: dict

        :param update: The update to apply
        :type update: dict
        """
        return database[Collections.USERS].update_many(
            query,
            update,
        )
    

    @classmethod
    def deactivate_one(self, query):
        """
        Method to deactivate a user

        :param query: The query to find the user
        :type query: dict

        :return: The user deactivated
        """
        return database[Collections.USERS].update_one(
            query,
            {
                "$set": {
                    "active": False,
                    "deactivated_at": datetime.now().isoformat()
                }
            },
        )
