from src.visualization import VisualizationFactory, VisualizationType


def main():
    # visualization = VisualizationFactory.create_visualization(VisualizationType.KEYBOARD)
    visualization = VisualizationFactory.create_visualization(VisualizationType.PID)
    visualization.run()


if __name__ == '__main__':
    main()
