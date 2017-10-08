import React, {Component} from 'react';

export default class Inn extends Component {
    constructor(props) {
        super(props);
    }

    onChange(e) {
        const value = (e.target.validity.valid) ? e.target.value : this.state.value;
        this.props.onChange(value);
    }

    render() {
        return (<input type='text' pattern='[0-9]*'
                       onInput={::this.onChange}
                       value={this.props.value}/>)
    }
}