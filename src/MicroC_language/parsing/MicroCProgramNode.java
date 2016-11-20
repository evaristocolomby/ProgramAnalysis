/**
 *
 * @author Evaristo
 */
public class MicroCProgramNode {
   String name;
   MicroCProgramNode children;
   MicroCProgramNode parent;
   Integer node_counter;

    public MicroCProgramNode(String name, MicroCProgramNode children, MicroCProgramNode parent, Integer node_counter) {
        this.name = name;
        this.children = children;
        this.parent = parent;
        this.node_counter = node_counter;
    }
    
    @Override
    public String toString() {
        return name;
    }
   
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public MicroCProgramNode getChildren() {
        return children;
    }

    public void setChildren(MicroCProgramNode children) {
        this.children = children;
    }

    public MicroCProgramNode getParent() {
        return parent;
    }

    public void setParent(MicroCProgramNode parent) {
        this.parent = parent;
    }

    public Integer getNode_counter() {
        return node_counter;
    }

    public void setNode_counter(Integer node_counter) {
        this.node_counter = node_counter;
    }
}