from flask import Flask, render_template, request
from pyahp import parse
import mcdm

app = Flask(__name__)

@app.route('/')
def people():
    return render_template('people.html')

@app.route('/criteria',methods = ['POST', 'GET'])
def criteria():
    result = int(request.form['people'])
    return render_template('criteria.html', result = result)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        #ahp weight
        ahp_matrix = [
            [1, 7, 3, 7],
            [1/7, 1, 1/3, 1],
            [1/3, 3, 1, 5],
            [1/7, 1, 1/5, 1]
        ]
        ahp_model = {
            "name": "AHP Model",
            "method": "approximate",
            "criteria": ["c1", "c2", "c3", "c4"],
            "subCriteria": {},
            "alternatives": ["a1", "a2", "a3", 'a4'],
            "preferenceMatrices": {
                "criteria": ahp_matrix,
                "alternatives:c1": ahp_matrix,
                "alternatives:c2": ahp_matrix,
                "alternatives:c3": ahp_matrix,
                "alternatives:c4": ahp_matrix
            }
        }

        #get priorities
        ahp = parse(ahp_model)
        priorities = ahp.get_priorities()

        #get user input
        user_input = request.form
        nama = []

        #create pair_wise matrix
        pair_wise_matrix = []
        for i in range(int(user_input['people'])):
            key1 = 'profesi' + str(i)
            key2 = 'umur' + str(i)
            key3 = 'health' + str(i)
            key4 = 'zone' + str(i)
            key5 = 'nama' +str(i)
            pair_wise_matrix.append([
                user_input[key1], 
                user_input[key2], 
                user_input[key3], 
                user_input[key4]
            ])
            nama.append([
                user_input[key1], 
                user_input[key2], 
                user_input[key3], 
                user_input[key4],
                user_input[key5]
            ])

        print(nama)
            
        #rank using SAW
        rank = mcdm.rank(pair_wise_matrix,
            w_vector = priorities,
            n_method = "Linear1",
            s_method = "SAW")

        print(rank)

        result = []        
        for i in rank:
            result.append(i[0].replace('a', ''))

        res_nama = []
        for i in result:
            res_nama.append(nama[int(i) - 1])      
                    
        return render_template("result.html", result = res_nama)

if __name__ == '__main__':
   app.run(debug = True)