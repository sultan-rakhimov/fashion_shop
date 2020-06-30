import React from 'react'
import classes from './css/Product.module.css'

export default function Product(props) {
    return (
        <div className={classes.product}>
            <em>{props.id}</em>
            <strong>{props.user_id}</strong>
            <h3>{props.title}</h3>
            <p>{props.description}</p>
            <p>{props.date}</p>
        </div>
    )
}
