import mysql.connector
import os


class sql_module:
    def __init__(self):
        # using os enviorn here might be smarter
        with open(os.path.expanduser("~/Desktop/secret/secret"), "r") as f:
            secret = f.read()
            secret = secret.split(",")
            f.close()

        self.host = secret[0]
        self.user = secret[1]
        self.password = secret[2]
        self.database = secret[3]
        # print(self.host, self.user, self.password, self.database)

        self.establish_connection()

    def establish_connection(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database="device-info"
            )
            self.mycursor = self.mydb.cursor()
        except Exception as e:
            raise SystemExit(e)

    def get_admin_details(self, username):
        sql_cmd = "select * from admin_users where username='%s'" % (username)
        try:
            self.mycursor.execute(sql_cmd)
            myresult = self.mycursor.fetchall()
            if (len(myresult) <= 0):
                return None
            return myresult[0]
        except Exception as e:
            print(e)
            return e

    def register_device(self, info):
        sql_cmd = "insert into pc_info (hostname, active, ip_address, mac_address, installed_os, os_version, cpu, ram_size) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.mycursor.execute(sql_cmd, info)
            self.mydb.commit()
            print(f"Successfully added {info[0]} in the database!")
            return True
        except Exception as e:
            print(f"Error adding {info[0]} to the database!\n** ERROR: {e}")
            return e

    def pull_device(self, hostname):
        sql_cmd = "SELECT * from pc_info WHERE hostname='%s'" % (hostname)
        try:
            self.mycursor.execute(sql_cmd)
            myresult = self.mycursor.fetchall()
            if (len(myresult) <= 0):
                print(f"Couldn't pull device: {hostname}")
                return None
            return myresult[0]
        except Exception as e:
            print(f"Unable to pull device: {hostname}")
            return e
    def modify_admin_cookie(self, admin_username, new_cookie):
        # for better security, it might be worth including 2FA
        if self.get_admin_details(admin_username) is None:
            return "Admin account was not found"
        try:
            sql_cmd = "UPDATE admin_users SET sessionid='%s' WHERE username='%s'"%(new_cookie, admin_username)
            self.mycursor.execute(sql_cmd)
            self.mydb.commit()
            return True
        except Exception as e:
            print(f"Failed to update session cookie for '{admin_username}'\n** ERROR: {e}")

            return False
    def search_by_session(self, session):
        sql_cmd = "select * from admin_users where sessionid='%s'"%(session)
        try:
            self.mycursor.execute(sql_cmd)
            myresult = self.mycursor.fetchall()
            print(myresult)
            if myresult is None:
                return None
            if (session == myresult[0][2]):
                return True
            return False
        except Exception as e:
            print(f"Unable to pull cookie.\n** ERROR: {e}")
            return None
    def device_re(self, hostname):
        sql_cmd = "delete from pc_info where hostname='%s'"%(hostname)
        try:
            self.mycursor.execute(sql_cmd)
            self.mydb.commit()
        except Exception as e:
            print(f"Failed to delete record.\n** ERROR: {e}")
            return False




# c = sql_module()
#insert into pc_info (hostname, active, ip_address, os_version, cpu, ram_size) 
# c.mycursor.execute("create table pc_info (hostname text not null, active int not null, ip_address text not null, os_version text not null, cpu text not null, ram_size text not null)")
# c.mycursor.execute("insert into pc_info (hostname, active, ip_address, os_version, cpu, ram_size) VALUES(%s,%s,%s, %s, %s, %s)", ("test", 0,"ip_addr", "Windows 20H21idk", "Intel ibitch", "69GB"))
# c.mydb.commit()
# b = c.pull_device("fr")
# a = c.modify_admin_cookie("admin", 'new_set_cookie')
# print(b)

