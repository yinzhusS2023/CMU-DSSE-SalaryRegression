import pickle


class ObjectManager:

    @staticmethod
    def write_object(filename, obj):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(obj, file)
                return True
        except Exception as e:
            print("Failed Writing Object: " + str(e))
            return False

    @staticmethod
    def read_object(filename):
        try:
            with open(filename, 'rb') as file:
                obj = pickle.load(file)
                return True, obj
        except Exception as e:
            print("Failed Reading Object: " + str(e))
            return False, None
