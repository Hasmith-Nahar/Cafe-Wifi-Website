def fetch_data():
    global cafes
    cafes.clear()
    all_cafes = db.session.query(Cafe, User) \
        .filter(Cafe.user_id == User.id) \
        .all()
    for cafe, user in all_cafes:
        cafe = cafe.to_dict()
        user = user.to_dict()
        cafe['author'] = user
        cafes.append(cafe)
    print(len(cafes), cafes)
    return cafes
 
# Handling Authorization for Delete a Cafe
 
@app.route('/report_closed/<int:cafe_id>', methods=['GET', 'DELETE'])
@login_required
def close_cafe(cafe_id):
    params = request.args.to_dict()
    try:
        req_api_key = params['api_key']
        print(req_api_key)
        if req_api_key != app.config['SECRET_KEY']:
            return jsonify(ResponseMessage.forbidden), 403
    except KeyError:
        return jsonify(ResponseMessage.forbidden), 403
    selected_cafe = Cafe.query.get(cafe_id)
    if selected_cafe is None:
        return jsonify(ResponseMessage.not_found_id), 404
    selected_cafe = selected_cafe.to_dict()
    if current_user.id != selected_cafe['user_id']:
        return jsonify(ResponseMessage.unauthorized), 401
    db.session.delete(selected_cafe)
    db.session.commit()
    return redirect(url_for('home'))
  
