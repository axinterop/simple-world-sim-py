from utils import CollisionStatus


class WorldListener:
    def __init__(self):
        self.events = []

    def record_event(self, d: str):
        self.events.append(d)

    def record_collision(self, c_s: CollisionStatus, this_o, other_o):
        event = ""

        if c_s == CollisionStatus.BREED:
            event = f"{this_o.class_info()} bred with another {
                other_o.class_info()}"
        elif c_s == CollisionStatus.KILL:
            event = f"{this_o.class_info()} killed {other_o.class_info()}"
        elif c_s == CollisionStatus.DIE:
            event = f"{this_o.class_info()} ran into {
                other_o.class_info()} and died"
        elif c_s == CollisionStatus.BLOCK_ATTACK:
            event = f"{other_o.class_info()} blocked attack from {
                this_o.class_info()}"
        elif c_s == CollisionStatus.ESCAPE:
            event = f"{other_o.class_info()} escaped from {
                this_o.class_info()}"
        elif c_s == CollisionStatus.AVOID_DEATH:
            event = f"{this_o.class_info()} avoided death from {
                other_o.class_info()}"
        elif c_s == CollisionStatus.BOOST_EATING:
            event = f"{this_o.class_info()} has eaten {
                other_o.class_name()} and became stronger"
        elif c_s == CollisionStatus.KILL_EATING:
            event = f"{this_o.class_info()} has eaten {
                other_o.class_name()} and died"
        elif c_s == CollisionStatus.UNDEFINED:
            event = f"Undefined collision between {
                this_o.class_info()} and {other_o.class_info()}"
        elif c_s == CollisionStatus.EATED:
            event = f"{this_o.class_info()} has eaten {other_o.class_name()}"

        if c_s != CollisionStatus.STAY:
            self.record_event(event)
