import React, {Component} from 'react';
import Select from 'react-select';
import 'react-select/dist/react-select.css';


export default class User extends Component {
    constructor(props) {
        super(props);
    }
	onChange (value) {
		this.props.onChange(value.value);
	}

	loadUsers (input) {
        let search = '';
        if (input) {
            search = `?search=${input}`;
        }
		return fetch(`/api/users/${search}`)
		.then((response) => response.json())
		.then((json) => {
            let options = [];
            for(let i = 0; i < json.length; i++) {
                let data = json[i];
                options.push({
                    value: data.id,
                    label: `${data.username} (${data.email}) ${data.get_full_name}`
                });
            }
			return { options: options };
		});
	}

    render() {
        return (
            <Select.Async
                isLoading={true}
                loadOptions={this.loadUsers}
                value={this.props.value}
                onChange={::this.onChange}
            />
        )
    }
}