/*!

=========================================================
* Black Dashboard React v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-react
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/black-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { useEffect } from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react plugin used to create charts
import { Line, Bar } from "react-chartjs-2";
import { makeStyles } from '@material-ui/core/styles';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import clsx from 'clsx';
import Collapse from '@material-ui/core/Collapse';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import { red } from '@material-ui/core/colors';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import FlashOnIcon from '@material-ui/icons/FlashOn';
import ScheduleIcon from '@material-ui/icons/Schedule';
import EuroIcon from '@material-ui/icons/Euro';
import CloseIcon from '@material-ui/icons/Close';

import { createMuiTheme } from '@material-ui/core/styles';

import Divider from '@material-ui/core/Divider';

import socketIOClient from "socket.io-client";

// reactstrap components
import {
  Button,
  ButtonGroup,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  Label,
  FormGroup,
  Input,
  Table,
  Row,
  Col,
  UncontrolledTooltip,
} from "reactstrap";

// core components
import {
  chartExample1,
  chartExample2,
  chartExample3,
  chartExample4,
} from "variables/charts.js";


const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#757ce8',
      main: '#3f50b5',
      dark: '#002884',
      contrastText: '#fff',
    },
    secondary: {
      light: '#ff7961',
      main: '#f44336',
      dark: '#ba000d',
      contrastText: '#000',
    },
  },
});


const useStyles = makeStyles({
  marker: {
    // backgroundColor: "blue",
    // width: 100,
    // margin: 10
  },
  colContent: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center"
  },
  iconRow: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    // backgroundColor: "#1d8cf8",
    // opacity: 0.2,
    margin: 10,
    height: 30,
  },
});

function FeedItem(props) {

  const ENDPOINT = "http://127.0.0.1:5000/socket";
  const classes = useStyles();

  const [expanded, setExpanded] = React.useState(false);
  const [notifications, setNotifications] = React.useState([]);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Card className={classes.root}>
      <CardHeader>
          <Row>
            <Col sm="12">
              <div className={classes.marker}>
                <CardTitle tag="h2">Notification #{props.id}</CardTitle>
              </div>
            </Col>
            {/* <Col sm="1">
              <CloseIcon 
                fontSize="large"
                style={{ color: "#FFFFFF" }}
              />
            </Col> */}
          </Row>
      </CardHeader>

      <CardContent>
        <Row>
          <Col xs="4">
            <div className={classes.colContent}>
              <Typography variant="h3">
                <FlashOnIcon 
                  fontSize="large"
                  color="primary"
                /> {props.impact}
              </Typography>
              <h5 className="card-category">Impact Score</h5>
            </div>
          </Col>

          <Col xs="4">
            <div className={classes.colContent}>
              <Typography variant="h3">
                <EuroIcon 
                  fontSize="large"
                  color="primary"
                />  {props.priceChange}
              </Typography>
              <h5 className="card-category">Relative Price Change</h5>
            </div>
          </Col>

          <Col xs="4">
            <div className={classes.colContent}>
              <Typography variant="h3">
                <ScheduleIcon 
                  fontSize="large"
                  color="primary"
                /> {props.timeWindow}
              </Typography>
              <h5 className="card-category">Effected Time Bucket</h5>
            </div>
          </Col>
        </Row>
      </CardContent>

      <div className={classes.iconRow} >
        <Button variant="outlined">Done</Button>
      </div>

      <div className={classes.iconRow} >
        <IconButton
          className={clsx(classes.expand, {
            [classes.expandOpen]: expanded,
          })}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon
            style={{ color: "#FFFFFF" }}
          />
        </IconButton>
      </div>
      
      <Divider variant="middle" />

      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>

          <Col xs="4">
            <div className={classes.colContent}>
              <Typography variant="h3">
                {props.timeWindow}
              </Typography>
              <h5 className="card-category">Effected Time Bucket</h5>
            </div>
          </Col>

          {/* <Typography paragraph>Method:</Typography>
          <Typography paragraph>
            Heat 1/2 cup of the broth in a pot until simmering, add saffron and set aside for 10
            minutes.
          </Typography>
          <Typography paragraph>
            Heat oil in a (14- to 16-inch) paella pan or a large, deep skillet over medium-high
            heat. Add chicken, shrimp and chorizo, and cook, stirring occasionally until lightly
            browned, 6 to 8 minutes. Transfer shrimp to a large plate and set aside, leaving chicken
            and chorizo in the pan. Add pimentón, bay leaves, garlic, tomatoes, onion, salt and
            pepper, and cook, stirring often until thickened and fragrant, about 10 minutes. Add
            saffron broth and remaining 4 1/2 cups chicken broth; bring to a boil.
          </Typography>
          <Typography paragraph>
            Add rice and stir very gently to distribute. Top with artichokes and peppers, and cook
            without stirring, until most of the liquid is absorbed, 15 to 18 minutes. Reduce heat to
            medium-low, add reserved shrimp and mussels, tucking them down into the rice, and cook
            again without stirring, until mussels have opened and rice is just tender, 5 to 7
            minutes more. (Discard any mussels that don’t open.)
          </Typography>
          <Typography>
            Set aside off of the heat to let rest for 10 minutes, and then serve.
          </Typography> */}
        </CardContent>
      </Collapse>
    </Card>
  );
}


function Dashboard(props) {
  const ENDPOINT = "http://127.0.0.1:5000/socket";

  const [bigChartData, setbigChartData] = React.useState("data1");
  const setBgChartData = (name) => {
    setbigChartData(name);
  };
  const [notifications, setNotifications] = React.useState([]);

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on("event", event => {
      console.log(event);
      setNotifications(notifications => [...notifications, event]);
    });
  }, []);
  return (
    <>
      <div className="content" theme={theme}>
        
        <Row>
          <Col xs="12">
            <Card className="card-chart">
              <CardHeader>
                <Row>
                  <Col className="text-left" sm="6">
                    <h5 className="card-category">Hourly Buckets (EUR)</h5>
                    <CardTitle tag="h2">Intraday Price</CardTitle>
                  </Col>
                  <Col sm="6">
                
                  </Col>
                </Row>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartExample1[bigChartData]}
                    options={chartExample1.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>

        <FeedItem
          id={1}
          impact={89}
          priceChange={"+22%"}
          timeWindow={"17H-18H"}
        />
        <FeedItem
          id={2}
          impact={75}
          priceChange={"+18%"}
          timeWindow={"18H-19H"}
        />
        <FeedItem
          id={3}
          impact={61}
          priceChange={"-13%"}
          timeWindow={"16H-17H"}
        />
        <FeedItem
          id={4}
          impact={42}
          priceChange={"+9%"}
          timeWindow={"20H-21H"}
        />

        {/* <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Wind Speed (m/s)</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-bell-55 text-info" /> 23.9
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartExample2.data}
                    options={chartExample2.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Temperature (°C)</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-delivery-fast text-primary" />{" "}
                  16.2
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Bar
                    data={chartExample3.data}
                    options={chartExample3.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Precipitation (mm)</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-send text-success" /> 12.3
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartExample4.data}
                    options={chartExample4.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row> */}
      </div>
    </>
  );
}

export default Dashboard;
