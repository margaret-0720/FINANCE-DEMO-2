from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock DB (가짜 계좌 데이터)
accounts = {
    "123-456": {"balance": 500000, "history": []},
    "999-111": {"balance": 200000, "history": []},
    "777-888": {"balance": 750000, "history": []}
    }

@app.post("/balance")
def balance():
    account = request.form.get("account")
    
    if account not in accounts:
        return jsonify({"message": "존재하지 않는 계좌번호입니다."})
    
    bal = accounts[account]["balance"]
    return jsonify({"message": f"{account} 잔액: {bal}원"})

@app.post("/transfer")
def transfer():
    from_acc = request.form.get("from_acc")
    to_acc = request.form.get("to_acc")
    amount = request.form.get("amount")

    # 입력 체크
    if not from_acc or not to_acc or not amount:
        return jsonify({"message": "모든 입력값을 입력하세요."})

    if from_acc not in accounts:
        return jsonify({"message": "출금 계좌가 존재하지 않습니다."})

    if to_acc not in accounts:
        return jsonify({"message": "입금 계좌가 존재하지 않습니다."})

    try:
        amount = int(amount)
    except:
        return jsonify({"message": "금액은 숫자로 입력하세요."})

    if amount <= 0:
        return jsonify({"message": "0원 이하 금액은 송금할 수 없습니다."})

    if accounts[from_acc]["balance"] < amount:
        return jsonify({"message": "잔액이 부족합니다."})

    # -----------------------------
    # 여기! 날짜 자동 생성 코드
    # -----------------------------
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    # 송금 처리
    accounts[from_acc]["balance"] -= amount
    accounts[to_acc]["balance"] += amount

    # 거래내역 기록
    accounts[from_acc]["history"].append({
        "date": today,           # ← 여기 자동 날짜 입력됨
        "type": "출금",
        "amount": amount,
        "other": to_acc
    })

    accounts[to_acc]["history"].append({
        "date": today,           # ← 동일
        "type": "입금",
        "amount": amount,
        "other": from_acc
    })

    return jsonify({"message": f"{amount}원이 성공적으로 송금되었습니다."})


@app.get("/transactions")
def transactions():
    # 모든 계좌의 기록을 단순히 합쳐서 반환 (포트폴리오용)
    output = []
    for acc in accounts:
        for h in accounts[acc]["history"]:
            output.append(h)
    return jsonify({"list": output})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

