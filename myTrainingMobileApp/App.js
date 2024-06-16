import { NavigationContainer } from "@react-navigation/native"
import { DrawerContentScrollView, DrawerItem, DrawerItemList, createDrawerNavigator } from "@react-navigation/drawer"
import Home from "./components/Home/Home";
import Login from "./components/User/Login";
import { useEffect, useState } from "react";
import API, { endpoints } from "./configs/API";

const Drawer = createDrawerNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Drawer.Navigator drawerContent={MyDrawerItem}>
        <Drawer.Screen name="Home" component={Home} options={{title: 'Hoạt Động'}} /> 
        <Drawer.Screen name="Login" component={Login} />         
      </Drawer.Navigator>
    </NavigationContainer>
  )
}

const MyDrawerItem = (props) => {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    const loadActivities = async () => {
      let res = await API.get(endpoints['activities'])
      setActivities(res.data.results);
    }
    loadActivities();
  }, [])

  return (
    <DrawerContentScrollView {...props}>
      <DrawerItemList {...props} />
      {activities.map(c => <DrawerItem label={c.name} key={c.id} 
                                                      onPress={() => props.navigation.navigate('Home', {actId: c.name})} />)}
    </DrawerContentScrollView>
  )
} 

export default App;