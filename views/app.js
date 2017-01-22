import React from 'react';
import ReactDOM from 'react-dom';
import { createStore } from 'redux';
import $ from "jquery";

import { get } from './api.jsx';

import MetricsGraphics from 'react-metrics-graphics';

const DEFAULT_NAME = 'fake_users1.json';

var defaultState = {
    graphs: new Map(),
    selected: DEFAULT_NAME
};

function changeBuilding(newBuilding) {
    return {
        type: 'CHANGE_BUILDING',
        newBuilding: newBuilding
    };
}


function formatApiResponse(apiResponse){
        var data = [];
        apiResponse.forEach(function(graphList){
            var graphData = [];
            graphList.forEach(function(obj){
                var oldDate = obj.date;
                obj.date = new Date(oldDate);
                graphData.push(obj)
            })
            data.push(graphData);
        })
        return data;
}


function hackDavisApp(state = defaultState, action) {
    switch (action.type) {
        case 'CHANGE_BUILDING':
            var newState = Object.assign({}, state);
            var newBuilding = action.newBuilding;
            newState.selected = newBuilding;
            if (!('graphs' in newState)){newState.graphs = {}}
            if (newBuilding in newState.graphs) {return newState}
            var newBuildingGraph = $.getJSON('static/data/' + newBuilding, function(data){
                var graphData = formatApiResponse(data);
                newState.graphs[newBuilding] = data;
                return newState;
            })
        default:
            return newState;
    }
}

var store = createStore(hackDavisApp, defaultState);

class BuildingSelect extends React.Component {

    onFilterChange(e) {
        store.dispatch(changeBuilding(e.target.value));
    }

    render() {
        return (
                <select onChange={this.onFilterChange}>
                    <option value='fake_users1.json'>fake_users1.json</option>
                    <option value='fake_users2.json'>fake_users2.json</option>
                </select>
            )
    }
}

class BuildingGraph extends React.Component {
   constructor() {
        super();
        this.state = {
            graph: [],
            name: DEFAULT_NAME,
            isLoading: false
        }
        store.dispatch(changeBuilding(DEFAULT_NAME));
        store.subscribe(() => {
            var newState = store.getState();
            var newBuilding = newState.selected;
            this.setState({
                graph: newState.graphs[newBuilding],
                name: newBuilding,
                isLoading: false
            });
        });
    };

    render() {
        if (this.state.graph === undefined){ this.state.graph = [] }
        if (this.state.isLoading) {
            return (
                    <p> The page is loading </p>
                )
        }
        return (
                <MetricsGraphics
                    title={this.state.name}
                    data={this.state.graph}
                    width={600}
                    height={250}
                    x_accessor="date"
                    y_accessor="value"
                    legend={['Line 1','Line 2','Line 3']}
                    legend_target='.legend'
                />
            )
    }
}

ReactDOM.render(
    <div>
        <BuildingSelect />
        <BuildingGraph />
    </div>,
    document.getElementById('main')
);
