import React, {Component} from 'react'
import User from '../components/User'
import Inn from '../components/Inn'
import Amount from '../components/Amount'
import 'react-select2-wrapper/css/select2.css'

export default class Form extends Component {
    constructor(props) {
        super(props)
        this.state = {
            user_id: null,
            inn: '',
            amount: '',
            resp_body: null,
            resp_status: null
        };
    }
    urlEncodeFormData(data) {
        const str = [];
        for (let p in data) {
            str.push(encodeURIComponent(p) + '=' + encodeURIComponent(data[p]));
        }
        return str.join('&');
    }
    onSubmit(e) {
        e.preventDefault();
        this.setState({resp_body: null, resp_status: null})
        let formData = {
            'from_user_id': this.state.user_id,
            'to_inn': this.state.inn,
            'amount': this.state.amount
        };
        formData = this.urlEncodeFormData(formData);
        fetch('/api/transfers/', {
            method: 'post',
            headers: {
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: formData
        })
        .then((resp) => {
            this.setState({resp_status: resp.status})
            return resp.json()
        }).then((data) =>{
            if (this.state.resp_status == 201) {
                this.setState({
                    user_id: null,
                    inn: '',
                    amount: '',
                    resp_body: data
                })
            } else {
                this.setState({
                    resp_body: data
                })
            }
        })
        .catch(function (error) {
            this.setState({resp_body: {non_field_errors: [error]}, resp_status: 500})
        }.bind(this));
    }

    onUserChange(value) {
        this.setState({user_id: value})
    }

    onInnChange(value) {
        this.setState({inn: value})
    }

    onAmountChange(value) {
        this.setState({amount: value})
    }

    render() {
        let resp_status = this.state.resp_status;
        let resp_body = this.state.resp_body;
        let msg = null;
        if (resp_status && resp_body) {
            if (resp_status == 201) {
                msg = (<div className='success'>
                    {resp_body.msg}<br />
                    From: {resp_body.from}<br />
                    To: {resp_body.to}<br />
                    Amount: {resp_body.amount}
                </div>);
            } else {
                let errors = [];
                let k = 0;
                for (let f in resp_body) {
                    let f_errs = [];
                    if (f != 'non_field_errors') {
                        f_errs = resp_body[f].map((err, i) => <li key={k+i}>{f}: {err}</li>);
                    } else {
                        f_errs = resp_body[f].map((err, i) => <li key={k+i}>{err}</li>);
                    }
                    errors = errors.concat(f_errs);
                    k += f_errs.length;
                }
                msg = (<ul className='errors'>{errors}</ul>);
            }
        }

        return (<form className='transfer-form' onSubmit={::this.onSubmit}>
            <h1>Make transfer</h1>

            <label>From user: <User value={this.state.user_id} onChange={::this.onUserChange}/></label>

            <label>To INN: <Inn value={this.state.inn} onChange={::this.onInnChange}/></label>
            <label>Amount: <Amount value={this.state.amount} onChange={::this.onAmountChange}/></label>
            <button type='submit' className='btn'>Submit</button>
            {msg}
        </form>)
    }
}

// Form.propTypes = {
//   name: PropTypes.string.isRequired
// }